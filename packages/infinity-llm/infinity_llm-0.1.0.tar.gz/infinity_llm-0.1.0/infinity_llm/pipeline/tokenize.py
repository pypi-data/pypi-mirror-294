from typing import List
import tiktoken
from transformers import GPT2TokenizerFast, AutoTokenizer
import cohere
from voyageai import Client as voyage_client
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.messages import UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.embedding.request import EmbeddingRequest

from infinity_llm import Provider, get_api_key, model_mapping


def tokenize_openai(model: str, text: str) -> List[str]:
    encoding = tiktoken.encoding_for_model(model)
    return encoding.encode(text)


def tokenize_voyage(model: str, text: str) -> List[str]:
    client = voyage_client(api_key=get_api_key(Provider.VOYAGE))
    tokenized = client.tokenize(text, model)
    return [token for sublist in tokenized for token in sublist]


def tokenize_cohere(model: str, text: str) -> List[str]:
    co = cohere.Client(api_key=get_api_key(Provider.COHERE))
    return co.tokenize(text=text, model=model)


def tokenize_anthropic(text) -> List[str]:
    tokenizer = GPT2TokenizerFast.from_pretrained("Xenova/claude-tokenizer")
    return tokenizer.encode(text)


def tokenize_mistral(model: str, text: str) -> List[str]:
    tokenizer = MistralTokenizer.from_model(model)

    if model == "mistral-embed":
        request = EmbeddingRequest(inputs=[text], model=model)
        return tokenizer.instruct_tokenizer.encode_embedding(request).tokens
    else:
        request = ChatCompletionRequest(messages=[UserMessage(content=text)])
        return tokenizer.encode_chat_completion(request).tokens


def tokenize_google(model: str, text: str) -> List[str]:
    tokenizer = AutoTokenizer.from_pretrained(model)
    return tokenizer.encode(text)


def tokenize_oss(model: str, text: str) -> List[str]:
    if model == "mistralai/Mistral-7B-Instruct-v0.1":
        return tokenize_mistral("open-mistral-7b", text)
    elif model in ["mixtral-8x7b-32768", "mistralai/Mixtral-8x7B-Instruct-v0.1"]:
        return tokenize_mistral("open-mixtral-8x7b", text)
    elif model == "mistralai/Mixtral-8x22B-Instruct-v0.1":
        return tokenize_mistral("open-mixtral-8x22b", text)
    elif model in ["gemma-7b-it", "google/gemma-7b-it"]:
        return tokenize_google("google/gemma-7b", text)
    elif model == "thenlper/gte-large":
        tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-large")
        return tokenizer(
            text, max_length=512, padding=True, truncation=True, return_tensors="pt"
        )
    elif model == "BAAI/bge-large-en-v1.5":
        tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-large-zh-v1.5")
        return tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    elif model == "mlabonne/NeuralHermes-2.5-Mistral-7B":
        return tokenize_mistral("open-mistral-7b", text)


def get_embed_input_tokens(request_json, provider: Provider) -> int:
    def get_text(inputs):
        if isinstance(inputs, str):
            return inputs
        elif isinstance(inputs, list):
            if all(isinstance(i, str) for i in inputs):
                return "".join(inputs)
            else:
                raise TypeError(
                    'Expected a list of strings for "inputs" field in embedding request'
                )
        else:
            raise TypeError(
                'Expected a list of strings for "inputs" field in embedding request'
            )

    if provider == Provider.OPENAI:
        return tokenize_openai(request_json["model"], get_text(request_json["input"]))
    elif provider == Provider.ANYSCALE:
        return tokenize_oss(request_json["model"], get_text(request_json["input"]))
    elif provider == Provider.MISTRAL:
        return tokenize_mistral(
            model=request_json["model"], text=get_text(request_json["input"])
        )
    elif provider == Provider.VOYAGE:
        return tokenize_voyage(model=request_json["model"], text=request_json["texts"])
    elif provider == Provider.COHERE:
        return tokenize_cohere(
            model=request_json["model"], text=get_text(request_json["texts"])
        )


def get_chat_prompt_tokens(request_json, provider: Provider) -> int:
    def get_text(messages):
        return "".join(value for message in messages for value in message.values())

    if provider == Provider.OPENAI:
        return tokenize_openai(
            request_json["model"], get_text(request_json["messages"])
        )
    elif provider == Provider.ANTHROPIC:
        return tokenize_anthropic(text=get_text(request_json["messages"]))
    elif provider in [Provider.GROQ, Provider.ANYSCALE]:
        return tokenize_oss(
            model=request_json["model"], text=get_text(request_json["messages"])
        )
    elif provider == Provider.MISTRAL:
        return tokenize_mistral(
            model=request_json["model"], text=get_text(request_json["messages"])
        )
    elif provider == Provider.COHERE:
        return tokenize_cohere(
            model=request_json["model"], text=get_text(request_json["messages"])
        )
