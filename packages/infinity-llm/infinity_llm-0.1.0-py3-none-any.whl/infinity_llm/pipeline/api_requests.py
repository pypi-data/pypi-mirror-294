from infinity_llm import Provider, get_api_key, Functionality


def get_request_header(provider: Provider) -> dict:
    api_key = get_api_key(provider)
    if provider == Provider.ANTHROPIC:
        return {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    elif provider in [
        Provider.OPENAI,
        Provider.MISTRAL,
        Provider.COHERE,
        Provider.GROQ,
        Provider.VOYAGE,
    ]:
        return {
            "Authorization": f"Bearer {api_key}",
            "content-type": "application/json",
        }

    else:
        raise ValueError(f"No request header for provider: {provider}")


def get_request_url(provider: Provider, functionality: Functionality) -> str:
    if provider == Provider.OPENAI:
        if functionality == Functionality.CHAT:
            return "https://api.openai.com/v1/chat/completions"
        elif functionality == "embedding":
            return "https://api.openai.com/v1/embeddings"
    elif provider == Provider.ANTHROPIC:
        if functionality == Functionality.CHAT:
            return "https://api.anthropic.com/v1/messages"
        elif functionality == Functionality.EMBEDDING:
            raise ValueError("Anthropic does not support embeddings")
    elif provider == Provider.MISTRAL:
        if functionality == Functionality.CHAT:
            return "https://api.mistral.ai/v1/chat/completions"
        elif functionality == Functionality.EMBEDDING:
            return "https://api.mistral.ai/v1/embeddings"
    elif provider == Provider.COHERE:
        if functionality == Functionality.CHAT:
            return "https://api.cohere.com/v1/chat"
        elif functionality == Functionality.EMBEDDING:
            return "https://api.cohere.com/v1/embed"
    elif provider == Provider.GROQ:
        if functionality == Functionality.CHAT:
            return "https://api.groq.com/openai/v1/chat/completions"
        elif functionality == Functionality.EMBEDDING:
            raise ValueError("Groq does not support embeddings")
    elif provider == Provider.VOYAGE:
        if functionality == Functionality.CHAT:
            raise ValueError("Voyage does not support chat")
        elif functionality == Functionality.EMBEDDING:
            return "https://api.voyageai.com/v1/embeddings"
    raise ValueError(
        f"Unsupported provider or functionality: {provider}, {functionality}"
    )
