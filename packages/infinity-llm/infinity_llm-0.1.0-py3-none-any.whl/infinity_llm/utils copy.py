import os, tiktoken
from typing import Dict, List, Optional, Union, NamedTuple
from collections import namedtuple
from instructor import Mode
from transformers import AutoTokenizer
from enum import Enum


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


# This file contains useful information about language models and utilities for converting text to tokens and reasoning about that

# Usage; calculated differently for chat vs. embedding models
EmbedUsage = namedtuple("EmbedUsage", ["input"])
ChatUsage = namedtuple("ChatUsage", ["prompt", "completion"])
CohereRerankUsage = namedtuple("CohereUsage", ["search"])

MaxInFlight = namedtuple("MaxInFlight", ["max_in_flight"])  # Anyscale rate limit
RateLimit = namedtuple("RateLimit", ["rpm", "tpm"])  # OpenAI rate limit
MistralRateLimit = namedtuple("MistralRateLimit", ["tpmin", "tpmonth"])
AnthropicRateLimit = namedtuple("AnthropicRateLimit", ["rpm", "tpm", "tpd"])
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
    "codestral-2405": ModelSpec(
        Provider.MISTRAL,
        32768,
        ChatUsage(1 * 1e-6, 3 * 1e-6),
        MistralRateLimit(500000, 1000000000),
    ),
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
    # "command": ModelSpec(Provider.COHERE, 4000, ChatUsage(2*1e-3), RateLimit(10000, 2147483647)),
    # "command-nightly": ModelSpec(Provider.COHERE, 128000, ChatUsage(2*1e-3), RateLimit(10000, 2147483647)),
    # "command-light": ModelSpec(Provider.COHERE, 4000, ChatUsage(2*1e-3), RateLimit(10000, 2147483647)),
    # "command-light-nightly": ModelSpec(Provider.COHERE, 4000, ChatUsage(2*1e-3), RateLimit(10000, 2147483647)),
    "embed-english-v3.0": ModelSpec(
        Provider.COHERE, 512, EmbedUsage(0.1 * 1e-6), RateLimit(10000, 2147483647)
    ),
    # "embed-english-light-v3.0": ModelSpec(Provider.COHERE, 512, EmbedUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "embed-multilingual-v3.0": ModelSpec(Provider.COHERE, 512, EmbedUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "embed-multilingual-light-v3.0": ModelSpec(Provider.COHERE, 512, EmbedUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "embed-english-v2.0": ModelSpec(Provider.COHERE, 512, EmbedUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "embed-english-light-v2.0": ModelSpec(Provider.COHERE, 512, EmbedUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "embed-multilingual-v2.0": ModelSpec(Provider.COHERE, 512, EmbedUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    "rerank-english-v3.0": ModelSpec(
        Provider.COHERE, 512, CohereRerankUsage(2 * 1e-3), RateLimit(10000, 2147483647)
    ),
    # "rerank-multilingual-v3.0": ModelSpec(Provider.COHERE, 512, CohereRerankUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "rerank-english-v2.0": ModelSpec(Provider.COHERE, 512, CohereRerankUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
    # "rerank-multilingual-v2.0": ModelSpec(Provider.COHERE, 512, CohereRerankUsage(0.00002*1e-3), RateLimit(10000, 2147483647)),
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
}


def get_tokens(model_name: str, prompt: str) -> List[int]:
    """
    Encodes a given prompt into a list of tokens using the specified model's encoder.
    """
    enc = tiktoken.encoding_for_model(model_name)
    max_tokens = model_mapping[model_name].context_length
    return enc.encode(prompt), max_tokens


def crop_text(
    model: str, text: str, max_tokens: Optional[int] = None, crop_from_top: bool = False
) -> str:
    """
    given text, crop it to max number of tokens and return as text
    """
    if "llama3" in model:
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    else:
        try:
            tokenizer = tiktoken.encoding_for_model(model)
        except Exception as e:
            print(f"Error: {e}")
            return text

    tokens = tokenizer.encode(text)
    if not max_tokens:
        max_tokens = (
            model_mapping[model].context_length - 800
        )  # heuristic for system, pydantic model, etc.
    if crop_from_top:
        cropped_tokens = tokens[-max_tokens:]
    else:
        cropped_tokens = tokens[:max_tokens]
    cropped_text = tokenizer.decode(cropped_tokens)
    return cropped_text


def crop_embed(text: str, max_tokens: int) -> str:
    """
    Crops the input text to a specified maximum number of tokens.
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    cropped_tokens = tokens[:max_tokens]
    cropped_text = tokenizer.decode(cropped_tokens)
    return cropped_text


def get_chat_urls(model_name: str) -> str:
    """
    Retrieves the chat URL for a given model name.
    """
    org = model_mapping[model_name].org
    model_to_chat_url = {
        "openai": "https://api.openai.com/v1/chat/completions",
        "anyscale": "https://api.endpoints.anyscale.com/v1/chat/completions",
        "anthropic": "https://api.anthropic.com/v1/messages",
        "cohere": "https://api.cohere.ai/v1/chat/completions",
        "voyage": "https://api.voyageai.com/v1/embeddings",
    }
    return model_to_chat_url[org]


def get_cost(completion: str, model_name: str) -> float:
    """
    Calculates the cost of a given completion based on the model name.
    """
    if model_mapping[model_name].org == "anthropic":
        prompt_toks = completion.usage.input_tokens
        completion_toks = completion.usage.output_tokens
    elif model_mapping[model_name].org == "voyage":
        return model_mapping[model_name].cost.input * completion
    else:
        # get usage
        prompt_toks = completion.usage.prompt_tokens
        completion_toks = completion.usage.completion_tokens

    return (model_mapping[model_name].cost.prompt * prompt_toks) + (
        model_mapping[model_name].cost.completion * completion_toks
    )
