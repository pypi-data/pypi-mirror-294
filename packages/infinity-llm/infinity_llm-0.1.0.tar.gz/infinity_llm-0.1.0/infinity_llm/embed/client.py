# very inspired by https://github.com/jxnl/instructor/blob/main/instructor/client.py

from __future__ import annotations

import openai
from openai.types.embedding import Embedding

from typing import Any, Callable, List, Union, overload, Tuple
from typing_extensions import Self
from infinity_llm.utils import Provider, get_provider
from collections.abc import Awaitable


class AnyEmbedder:
    client: Any | None
    create_fn: Callable[..., Any]
    provider: Provider

    def __init__(
        self,
        client: Any | None,
        create: Callable[..., Any],
        provider: Provider,
        **kwargs: Any,
    ):
        self.client = client
        self.create_fn = create
        self.provider = provider
        self.kwargs = kwargs

    @overload
    def create(
        self: AsyncAnyEmbedder,
        input: Union[str, List[str]],
        **kwargs: Any,
    ) -> Awaitable[List[Embedding]]: ...

    @overload
    def create(
        self: Self,
        input: Union[str, List[str]],
        **kwargs: Any,
    ) -> List[Embedding]: ...

    def create(self, input: Union[str, List[str]], **kwargs: Any) -> List[Embedding]:
        kwargs = self.handle_kwargs(kwargs)

        return self.create_fn(input=input, **kwargs)

    def handle_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        for key, value in self.kwargs.items():
            if key not in kwargs:
                kwargs[key] = value
        return kwargs


class AsyncAnyEmbedder(AnyEmbedder):
    client: Any | None
    embed_fn: Callable[..., Any]
    provider: Provider

    def __init__(
        self,
        client: Any | None,
        create: Callable[..., Any],
        provider: Provider,
        **kwargs: Any,
    ):
        self.client = client
        self.create_fn = create
        self.provider = provider
        self.kwargs = kwargs

    async def create(
        self, input: Union[str, List[str]], **kwargs: Any
    ) -> List[List[float]]:
        kwargs = self.handle_kwargs(kwargs)

        return await self.embed_fn(input=input, **kwargs)


@overload
def embed_from_openai(
    client: openai.OpenAI,
    **kwargs: Any,
) -> AnyEmbedder:
    pass


@overload
def embed_from_openai(
    client: openai.AsyncOpenAI,
    **kwargs: Any,
) -> AsyncAnyEmbedder:
    pass


def create_openai_wrapper(embed_func: Callable):
    """
    CreateEmbeddingResponse(data=[Embedding(embedding=[-0.02307623252272606,...], index=0, object='embedding')],
    model='text-embedding-ada-002',
    object='list',
    usage=Usage(prompt_tokens=11, total_tokens=11))
    """

    def wrapper(
        input: Union[str, List[str]], model: str, **kwargs: Any
    ) -> Tuple[List[List[float]], int]:
        response = embed_func(input=input, model=model, **kwargs)
        embed_dict = dict(sorted({d.index: d.embedding for d in response.data}.items()))
        return list(embed_dict.values()), response.usage.total_tokens

    return wrapper


def embed_from_openai(
    client: openai.OpenAI | openai.AsyncOpenAI,
    **kwargs: Any,
) -> AnyEmbedder | AsyncAnyEmbedder:
    """
    accepts Provider.OPENAI, Provider.ANYSCALE, Provider.TOGETHER, Provider.DATABRICKS
    """
    if hasattr(client, "base_url"):
        provider = get_provider(str(client.base_url))
    else:
        provider = Provider.OPENAI

    if not isinstance(client, (openai.OpenAI, openai.AsyncOpenAI)):
        import warnings

        warnings.warn(
            "Client should be an instance of openai.OpenAI or openai.AsyncOpenAI. Unexpected behavior may occur with other client types.",
            stacklevel=2,
        )

    wrapped_embed = create_openai_wrapper(client.embeddings.create)

    if isinstance(client, openai.OpenAI):
        return AnyEmbedder(
            client=client,
            create=wrapped_embed,
            provider=provider,
            **kwargs,
        )

    async def async_wrapped_embed(*args, **kwargs):
        return await wrapped_embed(*args, **kwargs)

    return AsyncAnyEmbedder(
        client=client,
        create=async_wrapped_embed,
        provider=provider,
        **kwargs,
    )
