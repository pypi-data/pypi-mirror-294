# inspired by https://github.com/jxnl/instructor/blob/main/instructor/client_cohere.py
from __future__ import annotations

import cohere
from typing import Any, List, Optional, overload, Union
from typing_extensions import Callable
import infinity_llm


def create_cohere_wrapper(embed_func: Callable):
    """
    id='f0d20803-71b8-412c-8f89-17907ed2da51'
    embeddings=[[0.023345947, ...]]
    texts=['this is an example sentence to embed using cohere.']
    meta=ApiMeta(api_version=ApiMetaApiVersion(version='1', is_deprecated=None, is_experimental=None), billed_units=ApiMetaBilledUnits(input_tokens=13.0, output_tokens=None, search_units=None, classifications=None), tokens=None, warnings=[])
    response_type='embeddings_floats'
    """

    def wrapper(
        input: Union[str, List[str]],
        model: str,
        input_type: str,
        embedding_types: Optional[str] = None,
        **kwargs: Any,
    ) -> Tuple[List[List[float]], int]:
        if isinstance(input, str):
            input = [input]
        assert len(input) <= 96, "Cohere can only embed up to 96 texts at a time"

        response = embed_func(
            texts=input,
            model=model,
            input_type=input_type,
            embedding_types=embedding_types,
            **kwargs,
        )
        return response.embeddings, int(response.meta.billed_units.input_tokens)

    return wrapper


@overload
def embed_from_cohere(
    client: cohere.Client,
    **kwargs: Any,
) -> infinity_llm.AnyEmbedder: ...


@overload
def embed_from_cohere(
    client: cohere.AsyncClient,
    **kwargs: Any,
) -> infinity_llm.AsyncAnyEmbedder: ...


def embed_from_cohere(
    client: cohere.Client | cohere.AsyncClient,
    **kwargs: Any,
):
    assert isinstance(
        client, (cohere.Client, cohere.AsyncClient)
    ), "Client must be an instance of cohere.Cohere or cohere.AsyncCohere"

    wrapped_embed = create_cohere_wrapper(client.embed)

    if isinstance(client, cohere.Client):
        return infinity_llm.AnyEmbedder(
            client=client,
            create=wrapped_embed,
            provider=infinity_llm.Provider.COHERE,
            **kwargs,
        )

    async def async_wrapped_embed(*args, **kwargs):
        return await wrapped_embed(*args, **kwargs)

    return infinity_llm.AsyncAnyEmbedder(
        client=client,
        create=async_wrapped_embed,
        provider=infinity_llm.Provider.COHERE,
        **kwargs,
    )
