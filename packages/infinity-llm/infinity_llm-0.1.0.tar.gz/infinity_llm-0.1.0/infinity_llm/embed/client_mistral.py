# from https://github.com/jxnl/instructor/blob/main/instructor/client_mistral.py
# Future imports to ensure compatibility with Python 3.9
from __future__ import annotations

import mistralai.client
import mistralai.async_client as mistralaiasynccli
import infinity_llm
from typing import overload, Any, List, Union, Tuple, Callable


def create_mistral_wrapper(embed_func: Callable):
    """
    id='a8b6383ac1764642b624260bb2c678b0'
    object='list'
    data=[EmbeddingObject(object='embedding', embedding=[-0.00262451171875,...], index=0)], [EmbeddingObject(...)...] model='mistral-embed'
    usage=UsageInfo(prompt_tokens=13, total_tokens=13, completion_tokens=0)
    """

    def wrapper(
        input: Union[str, List[str]], model: str, **kwargs: Any
    ) -> Tuple[List[List[float]], int]:
        if isinstance(input, str):
            input = [input]

        response = embed_func(input=input, model=model, **kwargs)
        embed_dict = dict(sorted({d.index: d.embedding for d in response.data}.items()))
        return list(embed_dict.values()), response.usage.total_tokens

    return wrapper


@overload
def embed_from_mistral(
    client: mistralai.client.MistralClient,
    **kwargs: Any,
) -> infinity_llm.AnyEmbedder: ...


@overload
def embed_from_mistral(
    client: mistralaiasynccli.MistralAsyncClient,
    **kwargs: Any,
) -> infinity_llm.AsyncAnyEmbedder: ...


def embed_from_mistral(
    client: mistralai.client.MistralClient | mistralaiasynccli.MistralAsyncClient,
    **kwargs: Any,
) -> infinity_llm.AnyEmbedder | infinity_llm.AsyncAnyEmbedder:
    assert isinstance(
        client, (mistralai.client.MistralClient, mistralaiasynccli.MistralAsyncClient)
    ), "Client must be an instance of mistralai.client.MistralClient or mistralai.async_cli.MistralAsyncClient"

    wrapped_embed = create_mistral_wrapper(client.embeddings)

    if isinstance(client, mistralai.client.MistralClient):
        return infinity_llm.AnyEmbedder(
            client=client,
            create=wrapped_embed,
            provider=infinity_llm.Provider.MISTRAL,
            **kwargs,
        )

    async def async_wrapped_embed(*args, **kwargs):
        return await wrapped_embed(*args, **kwargs)

    return infinity_llm.AsyncAnyEmbedder(
        client=client,
        create=async_wrapped_embed,
        provider=infinity_llm.Provider.MISTRAL,
        **kwargs,
    )
