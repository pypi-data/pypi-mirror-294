from typing import Union
from openai import OpenAI, AsyncOpenAI
import cohere
from mistralai.client import MistralClient
from mistralai.async_client import MistralAsyncClient
import voyageai

import infinity_llm
from infinity_llm.embed import AnyEmbedder, AsyncAnyEmbedder
from infinity_llm import Provider, get_api_key


def embed_from_any(
    provider: Provider,
    # model_name: str,
    async_client: bool = False,
) -> Union[AnyEmbedder, AsyncAnyEmbedder]:
    """
    Factory function to get the appropriate embedding client for a given provider.

    Args:
        provider (Provider): The provider to use.
        model_name (str): The name of the model to use.
        async_client (bool): Whether to return async clients. Defaults to False.

    Returns:
        Union[AnyEmbedder, AsyncAnyEmbedder]: The embedding client.
    """
    api_key = get_api_key(provider)

    if provider == Provider.OPENAI:
        raw_client = (
            AsyncOpenAI(api_key=api_key) if async_client else OpenAI(api_key=api_key)
        )
        return infinity_llm.embed_from_openai(raw_client)
    elif provider == Provider.COHERE:
        raw_client = (
            cohere.AsyncClient(api_key=api_key)
            if async_client
            else cohere.Client(api_key=api_key)
        )
        return infinity_llm.embed_from_cohere(raw_client)
    elif provider == Provider.VOYAGE:
        raw_client = (
            voyageai.AsyncClient(api_key=api_key)
            if async_client
            else voyageai.Client(api_key=api_key)
        )
        return infinity_llm.embed_from_voyage(raw_client)
    elif provider == Provider.MISTRAL:
        raw_client = (
            MistralAsyncClient(api_key=api_key)
            if async_client
            else MistralClient(api_key=api_key)
        )
        return infinity_llm.embed_from_mistral(raw_client)
    elif provider == Provider.ANYSCALE:
        raw_client = (
            AsyncOpenAI(
                base_url="https://api.endpoints.anyscale.com/v1",
                api_key=api_key,
            )
            if async_client
            else OpenAI(
                base_url="https://api.endpoints.anyscale.com/v1",
                api_key=api_key,
            )
        )
        return infinity_llm.embed_from_openai(raw_client)
    else:
        raise ValueError(
            f"Cannot create embedding client for unsupported provider: {provider}"
        )
