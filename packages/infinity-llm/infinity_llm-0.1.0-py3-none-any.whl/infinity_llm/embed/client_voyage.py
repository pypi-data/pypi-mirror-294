# from https://github.com/jxnl/instructor/blob/main/instructor/client_mistral.py
# Future imports to ensure compatibility with Python 3.9
from __future__ import annotations

import voyageai
import infinity_llm
from typing import overload, Any, List, Optional, Union, Tuple


def create_voyage_wrapper(embed_func):
    def wrapper(
        input: Union[str, List[str]],
        model: str,
        input_type: Optional[str] = None,
        truncation: Optional[str] = None,
    ) -> Tuple[List[List[float]], int]:
        assert len(input) <= 128, "Voyage can only embed up to 128 texts at a time"

        response = embed_func(
            texts=input, model=model, input_type=input_type, truncation=truncation
        )
        return response.embeddings, response.total_tokens

    return wrapper


@overload
def embed_from_voyage(
    client: voyageai.Client,
    **kwargs: Any,
) -> infinity_llm.AnyEmbedder: ...


@overload
def embed_from_voyage(
    client: voyageai.AsyncClient,
    **kwargs: Any,
) -> infinity_llm.AsyncAnyEmbedder: ...


def embed_from_voyage(
    client: voyageai.Client | voyageai.AsyncClient,
    **kwargs: Any,
) -> infinity_llm.AnyEmbedder | infinity_llm.AsyncAnyEmbedder:
    assert isinstance(
        client, (voyageai.Client, voyageai.AsyncClient)
    ), "Client must be an instance of voyageai.Client or voyageai.AsyncClient"

    wrapped_embed = create_voyage_wrapper(client.embed)

    if isinstance(client, voyageai.Client):
        return infinity_llm.AnyEmbedder(
            client=client,
            create=wrapped_embed,
            provider=infinity_llm.Provider.VOYAGE,
            **kwargs,
        )

    async def async_wrapped_embed(*args, **kwargs):
        return await wrapped_embed(*args, **kwargs)

    return infinity_llm.AsyncAnyEmbedder(
        client=client,
        create=async_wrapped_embed,
        provider=infinity_llm.Provider.VOYAGE,
        **kwargs,
    )
