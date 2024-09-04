from typing import Dict, Union, NamedTuple
from collections import namedtuple
from enum import Enum
import os


class Provider(Enum):
    OPENAI = "openai"
    VERTEXAI = "vertexai"
    ANTHROPIC = "anthropic"
    ANYSCALE = "anyscale"
    TOGETHER = "together"
    GROQ = "groq"
    MISTRAL = "mistral"
    COHERE = "cohere"
    GEMINI = "gemini"
    DATABRICKS = "databricks"
    VOYAGE = "voyage"
    UNKNOWN = "unknown"


# Usage; calculated differently for chat vs. embedding models
EmbedUsage = namedtuple("EmbedUsage", ["input"])
ChatUsage = namedtuple("ChatUsage", ["prompt", "completion"])
CohereRerankUsage = namedtuple("CohereUsage", ["search"])

MaxInFlight = namedtuple("MaxInFlight", ["max_in_flight"])  # Anyscale rate limit
RateLimit = namedtuple("RateLimit", ["rpm", "tpm"])  # OpenAI rate limit
MistralRateLimit = namedtuple("MistralRateLimit", ["tpm", "tpmonth"])
AnthropicRateLimit = namedtuple("AnthropicRateLimit", ["rpm", "tpm", "tpd"])
GeminiRateLimit = namedtuple("GeminiRateLimit", ["rpm", "tpm", "rpd"])
GroqRateLimit = namedtuple("GroqRateLimit", ["rpm", "tpm", "tpd"])


class ModelSpec(NamedTuple):
    provider: Provider
    context_length: int
    cost: Union[EmbedUsage, ChatUsage, CohereRerankUsage]
    limit: Union[
        MaxInFlight, RateLimit, MistralRateLimit, AnthropicRateLimit, GroqRateLimit
    ]


# last updated 4/24/24
model_mapping: Dict[str, ModelSpec] = {
    # embedding models
    "text-embedding-3-small": ModelSpec(
        Provider.OPENAI, 8192, EmbedUsage(0.02 * 1e-3), RateLimit(5000, 5000000)
    ),  # dim 1536
    "text-embedding-3-large": ModelSpec(
        Provider.OPENAI, 8192, EmbedUsage(0.13 * 1e-3), RateLimit(5000, 5000000)
    ),  # dim 3072
    "text-embedding-ada-002": ModelSpec(
        Provider.OPENAI, 8192, EmbedUsage(0.1 * 1e-6), RateLimit(5000, 5000000)
    ),  # dim 3072
    # core gpt 4 models
    "gpt-4o": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(5.0 * 1e-6, 15.0 * 1e-6),
        RateLimit(5000, 600000),
    ),
    "gpt-4o-2024-05-13": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(5.0 * 1e-6, 15.0 * 1e-6),
        RateLimit(5000, 600000),
    ),
    "gpt-4-turbo": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(10.0 * 1e-6, 30.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-4-turbo-2024-04-09": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(10.0 * 1e-6, 30.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-4-turbo-preview": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(10.0 * 1e-6, 30.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-4-0125-preview": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(10.0 * 1e-6, 30.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-4-1106-preview": ModelSpec(
        Provider.OPENAI,
        128000,
        ChatUsage(10.0 * 1e-6, 30.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-4": ModelSpec(
        Provider.OPENAI,
        8192,
        ChatUsage(30.0 * 1e-6, 60.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-4-0613": ModelSpec(
        Provider.OPENAI,
        8192,
        ChatUsage(30.0 * 1e-6, 60.0 * 1e-6),
        RateLimit(5000, 80000),
    ),
    "gpt-3.5-turbo-0125": ModelSpec(
        Provider.OPENAI,
        16385,
        ChatUsage(0.5 * 1e-6, 1.5 * 1e-6),
        RateLimit(3500, 160000),
    ),
    "gpt-3.5-turbo": ModelSpec(
        Provider.OPENAI,
        16385,
        ChatUsage(0.5 * 1e-6, 1.5 * 1e-6),
        RateLimit(3500, 160000),
    ),
    "gpt-3.5-turbo-instruct": ModelSpec(
        "openai", 4096, ChatUsage(1.5 * 1e-6, 2 * 1e-6), RateLimit(3500, 160000)
    ),
    "gpt-3.5-turbo-1106": ModelSpec(
        Provider.OPENAI,
        16385,
        ChatUsage(1.0 * 1e-6, 2.0 * 1e-6),
        RateLimit(3500, 160000),
    ),
    # anyscale
    "mistralai/Mistral-7B-Instruct-v0.1": ModelSpec(
        Provider.ANYSCALE, 32768, ChatUsage(0.15 * 1e-6, 0.15 * 1e-6), MaxInFlight(30)
    ),
    "mistralai/Mixtral-8x7B-Instruct-v0.1": ModelSpec(
        Provider.ANYSCALE, 32768, ChatUsage(0.90 * 1e-6, 0.90 * 1e-6), MaxInFlight(30)
    ),
    "mistralai/Mixtral-8x22B-Instruct-v0.1": ModelSpec(
        Provider.ANYSCALE, 64000, ChatUsage(0.50 * 1e-6, 0.50 * 1e-6), MaxInFlight(30)
    ),
    "meta-llama/Meta-Llama-3-8B-Instruct": ModelSpec(
        Provider.ANYSCALE, 8192, ChatUsage(0.15 * 1e-6, 0.15 * 1e-6), MaxInFlight(30)
    ),
    "meta-llama/Llama-3-70b-chat-hf": ModelSpec(
        Provider.ANYSCALE, 8192, ChatUsage(1 * 1e-6, 1 * 1e-6), MaxInFlight(30)
    ),
    "codellama/CodeLlama-70b-Instruct-hf": ModelSpec(
        Provider.ANYSCALE, 16000, ChatUsage(1 * 1e-6, 1 * 1e-6), MaxInFlight(30)
    ),
    "google/gemma-7b-it": ModelSpec(
        Provider.ANYSCALE, 8192, ChatUsage(0.15 * 1e-6, 0.15 * 1e-6), MaxInFlight(30)
    ),
    "mlabonne/NeuralHermes-2.5-Mistral-7B": ModelSpec(
        Provider.ANYSCALE, 32768, ChatUsage(0.15 * 1e-6, 0.15 * 1e-6), MaxInFlight(30)
    ),
    "thenlper/gte-large": ModelSpec(
        Provider.ANYSCALE, 512, EmbedUsage(0.90 * 1e-6), MaxInFlight(30)
    ),
    "BAAI/bge-large-en-v1.5": ModelSpec(
        Provider.ANYSCALE, 8192, EmbedUsage(0.90 * 1e-6), MaxInFlight(30)
    ),
    # mistral
    "open-mistral-7b": ModelSpec(
        Provider.MISTRAL,
        32768,
        ChatUsage(0.25 * 1e-6, 0.25 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    "open-mixtral-8x7b": ModelSpec(
        Provider.MISTRAL,
        32768,
        ChatUsage(0.7 * 1e-6, 0.7 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    "open-mixtral-8x22b": ModelSpec(
        Provider.MISTRAL,
        64000,
        ChatUsage(2 * 1e-6, 6 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    "mistral-small-latest": ModelSpec(
        Provider.MISTRAL,
        32768,
        ChatUsage(1 * 1e-6, 3 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    "mistral-medium-latest": ModelSpec(
        Provider.MISTRAL,
        32768,
        ChatUsage(2.7 * 1e-6, 8.1 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    "mistral-large-latest": ModelSpec(
        Provider.MISTRAL,
        32768,
        ChatUsage(4 * 1e-6, 12 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    "mistral-embed": ModelSpec(
        Provider.MISTRAL,
        8192,
        EmbedUsage(0.1 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
    # "codestral-2405": ModelSpec(Provider.MISTRAL, 32768, ChatUsage(1*1e-6, 3*1e-6), MistralRateLimit(500000, 1000000000)),
    # anthropic
    "claude-3-opus-20240229": ModelSpec(
        Provider.ANTHROPIC,
        200000,
        ChatUsage(15 * 1e-6, 75 * 1e-6),
        AnthropicRateLimit(4000, 400000, 10000000),
    ),
    "claude-3-sonnet-20240229": ModelSpec(
        Provider.ANTHROPIC,
        200000,
        ChatUsage(3 * 1e-6, 15 * 1e-6),
        AnthropicRateLimit(4000, 400000, 50000000),
    ),
    "claude-3-5-sonnet-20240620": ModelSpec(
        Provider.ANTHROPIC,
        200000,
        ChatUsage(3 * 1e-6, 15 * 1e-6),
        AnthropicRateLimit(4000, 400000, 50000000),
    ),
    "claude-3-haiku-20240307": ModelSpec(
        Provider.ANTHROPIC,
        200000,
        ChatUsage(0.25 * 1e-6, 1.25 * 1e-6),
        AnthropicRateLimit(4000, 400000, 100000000),
    ),
    # groq # NOTE: currently on free plan
    "llama3-8b-8192": ModelSpec(
        Provider.GROQ,
        8192,
        ChatUsage(0.05 * 1e-6, 0.08 * 1e-6),
        GroqRateLimit(30, 14400, 30000),
    ),
    "llama3-70b-8192": ModelSpec(
        Provider.GROQ,
        8192,
        ChatUsage(0.59 * 1e-6, 0.79 * 1e-6),
        GroqRateLimit(30, 14400, 6000),
    ),
    "mixtral-8x7b-32768": ModelSpec(
        Provider.GROQ,
        32768,
        ChatUsage(0.24 * 1e-6, 0.24 * 1e-6),
        GroqRateLimit(30, 14400, 5000),
    ),
    "gemma-7b-it": ModelSpec(
        Provider.GROQ,
        8192,
        ChatUsage(0.07 * 1e-6, 0.07 * 1e-6),
        GroqRateLimit(30, 14400, 15000),
    ),
    # cohere
    # rate limit: 10000 requests per minute, no TPM rate limit (used max value for 32-bit int)
    "command-r-plus": ModelSpec(
        Provider.COHERE,
        200000,
        ChatUsage(3.0 * 1e-6, 15.0 * 1e-6),
        RateLimit(10000, 2147483647),
    ),
    "command-r": ModelSpec(
        Provider.COHERE,
        128000,
        ChatUsage(0.5 * 1e-6, 1.5 * 1e-6),
        RateLimit(10000, 2147483647),
    ),
    "embed-english-v3.0": ModelSpec(
        Provider.COHERE, 512, EmbedUsage(0.1 * 1e-6), RateLimit(10000, 2147483647)
    ),
    "rerank-english-v3.0": ModelSpec(
        Provider.COHERE, 512, CohereRerankUsage(2 * 1e-3), RateLimit(10000, 2147483647)
    ),
    # voyage
    "voyage-large-2-instruct": ModelSpec(
        Provider.VOYAGE, 1600, EmbedUsage(0.12 * 1e-6), RateLimit(300, 1000000)
    ),
    "voyage-finance-2": ModelSpec(
        Provider.VOYAGE, 1024, EmbedUsage(0.12 * 1e-6), RateLimit(300, 1000000)
    ),
    "voyage-multilingual-2": ModelSpec(
        Provider.VOYAGE, 1024, EmbedUsage(0.12 * 1e-6), RateLimit(300, 1000000)
    ),
    "voyage-law-2": ModelSpec(
        Provider.VOYAGE, 1600, EmbedUsage(0.12 * 1e-6), RateLimit(300, 1000000)
    ),
    "voyage-code-2": ModelSpec(
        Provider.VOYAGE, 1536, EmbedUsage(0.12 * 1e-6), RateLimit(300, 1000000)
    ),
    "voyage-large-2": ModelSpec(
        Provider.VOYAGE, 1536, EmbedUsage(0.12 * 1e-6), RateLimit(300, 1000000)
    ),
    "voyage-2": ModelSpec(
        Provider.VOYAGE, 1024, EmbedUsage(0.1 * 1e-6), RateLimit(300, 1000000)
    ),
    "rerank-1": ModelSpec(
        Provider.VOYAGE, 8000, CohereRerankUsage(0.05 * 1e-6), RateLimit(100, 2000000)
    ),
    "rerank-lite-1": ModelSpec(
        Provider.VOYAGE, 4000, CohereRerankUsage(0.02 * 1e-6), RateLimit(100, 2000000)
    ),
    # gemini
    "models/gemini-1.5-pro": ModelSpec(Provider.GEMINI, 2097152, ChatUsage(3.5*1e-6, 10.5*1e-6), RateLimit(360, 4000000)),
    "models/gemini-1.5-flash": ModelSpec(Provider.GEMINI, 1048576, ChatUsage(0.075*1e-6, 0.3*1e-6), RateLimit(1000, 4000000)),
    "models/gemini-1.0-pro": ModelSpec(Provider.GEMINI, 2097152, ChatUsage(0.5*1e-6, 1.5*1e-6), GeminiRateLimit(360, 120000, 300000)),
    "models/text-embedding-004": ModelSpec(Provider.GEMINI, 2048, EmbedUsage(0.00001 * 1e-6), RateLimit(100000000, 1500)), # no tpm rate limit
}


def get_api_key(provider: Provider):
    """
    Fetches the API key for a given model provider
    """
    model_to_api_key = {
        Provider.OPENAI: os.getenv("OPENAI_API_KEY"),
        Provider.ANTHROPIC: os.getenv("ANTHROPIC_API_KEY"),
        Provider.ANYSCALE: os.getenv("ANYSCALE_API_KEY"),
        Provider.COHERE: os.getenv("COHERE_API_KEY"),
        Provider.VOYAGE: os.getenv("VOYAGE_API_KEY"),
        Provider.GROQ: os.getenv("GROQ_API_KEY"),
        Provider.MISTRAL: os.getenv("MISTRAL_API_KEY"),
        Provider.GEMINI: os.getenv("GOOGLE_API_KEY"),
    }
    assert provider in model_to_api_key, f"Provider '{provider}' is not recognized."
    return model_to_api_key[provider]


def get_provider(base_url: str) -> Provider:
    if "anyscale" in str(base_url):
        return Provider.ANYSCALE
    elif "together" in str(base_url):
        return Provider.TOGETHER
    elif "anthropic" in str(base_url):
        return Provider.ANTHROPIC
    elif "groq" in str(base_url):
        return Provider.GROQ
    elif "voyage" in str(base_url):
        return Provider.VOYAGE
    elif "openai" in str(base_url):
        return Provider.OPENAI
    elif "mistral" in str(base_url):
        return Provider.MISTRAL
    elif "cohere" in str(base_url):
        return Provider.COHERE
    elif "gemini" in str(base_url):
        return Provider.GEMINI
    elif "databricks" in str(base_url):
        return Provider.DATABRICKS
    elif "vertexai" in str(base_url):
        return Provider.VERTEXAI
    return Provider.UNKNOWN
