# infinity-llm: Use any LLM API

infinity-llm is a collection of Python tools to make LLM APIs plug-and-play for fast, easy experimentation.
I use this in my own projects today, but it's still very much a work in progress. I'm trying to strike 
the balance between simplicity and modularity, so if you have ideas feel free to message me or submit a PR!

[![Twitter Follow](https://img.shields.io/twitter/follow/markycasty?style=social)](https://twitter.com/markycasty)

## Key Features

- **Chat Completion**: Mostly a wrapper around [jxnl/instructor](https://github.com/jxnl/instructor), supports a/sync chat completion and streaming for structured and unstructured chat completions.
- **Embeddings/Rerankers**: Easily use a slew of embedding and reranking models
- **Asynchronous Workloads**: Run all chat completion and embedding workloads in massively parallel fashion without worrying about rate limits. Nice for ETL pipelines.
- **OpenAI Batch Jobs**: Run large scale batch jobs with OpenAI's batch API.

## Chat Completion

All types of chat completions are made easy!

1. Make a client
```python
from infinity_llm import from_any, Provider

client = from_any(
    provider=Provider.OPENAI, 
    model_name="gpt-4o", 
    async_client=False
    )
```

2. Choose between a/sync un/structured response with/without streaming

```python
# synchronous, unstructured response without streaming 
# (aka a standard chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a friend."},
        {"role": "user", "content": "Tell me about your day."}
    ],
    response_model=None # No response model means unstructured response
)
```

## Embeddings/Rerankers
```python
from infinity_llm import Provider, embed_from_any

# Create a Cohere embedding client
client = embed_from_any(Provider.COHERE)

# Example text to embed
text = "This is an example sentence to embed using Cohere."

# Get the embedding
embeddings, total_tokens = client.create(input=text, model="embed-english-v3.0", input_type="clustering")


print(f"Number of embeddings: {len(embeddings)}")
# > Number of embeddings: 1
print(f"Embedding dimension: {len(embeddings[0])}")
# > Embedding dimension: 1536
print(f"Usage: {total_tokens}")
# > Usage: 13
```
