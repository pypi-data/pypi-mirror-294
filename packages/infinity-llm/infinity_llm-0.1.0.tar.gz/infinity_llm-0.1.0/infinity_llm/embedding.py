from typing import List, Tuple, Optional, Iterable
import os, sys, torch, tiktoken, asyncio
from transformers import AutoTokenizer, AutoModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from llmOps.utils import model_mapping


def get_llm_embedder_task(task: str, type: str) -> str:
    instructions = {
        "qa": {
            "query": "Represent this query for retrieving relevant documents: ",
            "key": "Represent this document for retrieval: ",
        },
        "icl": {
            "query": "Convert this example into vector to look for useful examples: ",
            "key": "Convert this example into vector for retrieval: ",
        },
        "chat": {
            "query": "Embed this dialogue to find useful historical dialogues: ",
            "key": "Embed this historical dialogue for retrieval: ",
        },
        "lrlm": {
            "query": "Embed this text chunk for finding useful historical chunks: ",
            "key": "Embed this historical text chunk for retrieval: ",
        },
        "tool": {
            "query": "Transform this user request for fetching helpful tool descriptions: ",
            "key": "Transform this tool description for retrieval: ",
        },
        "convsearch": {
            "query": "Encode this query and context for searching relevant passages: ",
            "key": "Encode this passage for retrieval: ",
        },
        "email": {
            "query": "Encode this query and context for searching relevant emails: ",
            "key": "Encode this email for retrieval: ",
        },
    }
    return instructions[task][type]


def get_tqdm_iterable(items: Iterable, show_progress: bool, desc: str) -> Iterable:
    """
    Optionally get a tqdm iterable. Ensures tqdm.auto is used.
    """
    _iterator = items
    if show_progress:
        try:
            from tqdm.auto import tqdm

            return tqdm(items, desc=desc)
        except ImportError:
            pass
    return _iterator


def setup_llm_embedder(model: str) -> None:
    """returns model, tokenizer, max_tokens, embedder function"""
    model_nn = AutoModel.from_pretrained(model).eval()
    tokenizer = AutoTokenizer.from_pretrained(model)
    max_tokens = 512
    return model_nn, tokenizer, max_tokens


def run_llm_embedder(
    model: AutoModel,
    tokenizer: AutoTokenizer,
    embed_str: List[str],
    max_tokens: int,
    overlap_window: Optional[None],
    batch_size: int,
    **kwargs,
) -> Tuple[torch.Tensor, float]:
    batch, tensors = [], []
    queue_with_progress = enumerate(
        get_tqdm_iterable(embed_str, kwargs["show_progress"], "Generating embeddings")
    )
    for idx, text in queue_with_progress:
        batch.append(text)
        if idx == len(embed_str) - 1 or len(batch) == batch_size:
            # Encode for a specific task (qa, icl, chat, lrlm, tool, convsearch)
            task, type = kwargs.get("task", "icl"), kwargs.get("type", "key")
            prepend_string = get_llm_embedder_task(task, type)
            # tokenize the task and the input
            encoded_prepend = tokenizer(
                prepend_string, padding=True, return_tensors="pt"
            )  # 1 X T
            encoded_input = tokenizer(
                embed_str, padding=True, return_tensors="pt"
            )  # tokenize -> B x T

            # remove 101 ending token from task tokens
            prepend_input_id = encoded_prepend["input_ids"][:, :-1]
            prepend_token_type_ids = encoded_prepend["token_type_ids"][:, :-1]
            prepend_attention_mask = encoded_prepend["attention_mask"][:, :-1]

            # remove starting 101 token from text tokens
            input_ids = encoded_input["input_ids"][:, 1:]
            token_type_ids = encoded_input["token_type_ids"][:, 1:]
            attention_mask = encoded_input["attention_mask"][:, 1:]
            # take the task into account for chunk length
            max_tokens -= len(encoded_prepend["input_ids"].flatten())
            # chunk text into batches if text is longer than max token length
            chunk_input_ids = chunk_tensors(
                input_ids, max_tokens, overlap_window
            )  # tokens
            chunk_token_type_ids = chunk_tensors(
                token_type_ids, max_tokens, overlap_window
            )  # 1=question, 0=context
            chunk_attention_mask = chunk_tensors(
                attention_mask, max_tokens, overlap_window
            )  # 1=attend, 0=dont

            # concatenate prefix with sequence
            def concat_sequence(
                prefix: torch.Tensor, sequence: torch.Tensor
            ) -> torch.Tensor:
                """concatenate task with each piece of text"""
                return torch.cat(
                    (prefix.expand(sequence.shape[0], -1), sequence), dim=1
                )

            chunk_input_ids = concat_sequence(prepend_input_id, chunk_input_ids)
            chunk_token_type_ids = concat_sequence(
                prepend_token_type_ids, chunk_token_type_ids
            )
            chunk_attention_mask = concat_sequence(
                prepend_attention_mask, chunk_attention_mask
            )

            # embed and cls pool
            with torch.no_grad():
                model_output = model(
                    input_ids=chunk_input_ids,
                    token_type_ids=chunk_token_type_ids,
                    attention_mask=chunk_attention_mask,
                )
                sentence_embeddings = model_output[0][:, 0]
            # normalize embeddings
            embedding = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
            # return mean across chunks
            num_chunks = int(
                chunk_input_ids.shape[0] / encoded_input["input_ids"].shape[0]
            )
            mean_embeddings = torch.mean(
                embedding.view(num_chunks, encoded_input["input_ids"].shape[0], -1),
                dim=0,
            )
            tensors.extend(mean_embeddings)
            batch = []
    return tensors, 0.0


def setup_ada(model: str) -> None:
    """returns openai client, tokenizer, max_token_length"""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tokenizer = tiktoken.encoding_for_model(model)
    max_token_length = 8191
    return client, tokenizer, max_token_length


def setup_ada_normal(model: str) -> None:
    """returns openai client, tokenizer, max_token_length"""
    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tokenizer = tiktoken.encoding_for_model(model)
    max_token_length = 8191
    return client, tokenizer, max_token_length


def setup_voyage(model: str) -> None:
    """returns voyage client, tokenizer, context window"""
    import voyageai

    client = voyageai.AsyncClient()
    max_tokens = model_mapping[model].context_length
    tokenizer = AutoTokenizer.from_pretrained("voyageai/voyage")
    return client, tokenizer, max_tokens


def run_ada(
    client: str,
    model_name: str,
    tokenizer: tiktoken.core.Encoding,
    embed_str: List[str],
    max_tokens: int,
    overlap_window: int = None,
    **kwargs,
) -> Tuple[torch.Tensor, float]:
    """Accepts multidimensional array of strings, batch processes with asyncio"""
    # tokenize + pad, chunk, and untokenize to resize the strings
    max_len = max(len(tokenizer.encode(string)) for string in embed_str)
    encoded_input = torch.tensor(
        [
            tokenizer.encode(string) + [0] * (max_len - len(tokenizer.encode(string)))
            for string in embed_str
        ]
    )
    chunk_input_ids = chunk_tensors(encoded_input, max_tokens, overlap_window)
    chunk_input_strings = [tokenizer.decode(id) for id in chunk_input_ids.tolist()]

    async def embed_string(text: str):
        """async OpenAI Call"""
        return await client.embeddings.create(input=text, model=model_name)

    async def gather():
        """gather OpenAI responses"""
        get_responses = [embed_string(string) for string in chunk_input_strings]
        responses = await asyncio.gather(*get_responses)
        return responses

    responses = asyncio.run(gather())
    embeddings = [response.data[0].embedding for response in responses]
    usage = [response.usage for response in responses]

    # return mean across chunks
    embeddings = torch.tensor(embeddings)
    num_chunks = int(chunk_input_ids.shape[0] / encoded_input.shape[0])
    mean_embeddings = torch.mean(
        embeddings.view(num_chunks, encoded_input.shape[0], -1), dim=0
    )
    return mean_embeddings, usage


def run_ada_normal(
    client: str,
    model_name: str,
    tokenizer: tiktoken.core.Encoding,
    embed_str: List[str],
    max_tokens: int,
    overlap_window: int = None,
    **kwargs,
) -> Tuple[torch.Tensor, float]:
    """Accepts multidimensional array of strings, batch processes with asyncio"""
    # tokenize + pad, chunk, and untokenize to resize the strings
    max_len = max(len(tokenizer.encode(string)) for string in embed_str)
    encoded_input = torch.tensor(
        [
            tokenizer.encode(string) + [0] * (max_len - len(tokenizer.encode(string)))
            for string in embed_str
        ]
    )
    chunk_input_ids = chunk_tensors(encoded_input, max_tokens, overlap_window)
    chunk_input_strings = [tokenizer.decode(id) for id in chunk_input_ids.tolist()]

    def embed_string(text: str):
        """async OpenAI Call"""
        return client.embeddings.create(input=text, model=model_name)

    def gather():
        """gather OpenAI responses"""
        responses = [embed_string(string) for string in chunk_input_strings]
        return responses

    responses = gather()
    embeddings = [response.data[0].embedding for response in responses]
    usage = [response.usage for response in responses]

    # return mean across chunks
    embeddings = torch.tensor(embeddings)
    num_chunks = int(chunk_input_ids.shape[0] / encoded_input.shape[0])
    mean_embeddings = torch.mean(
        embeddings.view(num_chunks, encoded_input.shape[0], -1), dim=0
    )
    return mean_embeddings, usage


async def run_voyage(
    client: str,
    model_name: str,
    tokenizer: tiktoken.core.Encoding,
    embed_str: List[str],
    max_tokens: int,
    overlap_window: int = None,
    **kwargs,
) -> Tuple[torch.Tensor, float]:
    """Accepts multidimensional array of strings, batch processes with asyncio"""
    # tokenize + pad, chunk, and untokenize to resize the strings
    max_len = max(len(tokenizer.encode(string)) for string in embed_str)
    encoded_input = torch.tensor(
        [
            tokenizer.encode(string) + [0] * (max_len - len(tokenizer.encode(string)))
            for string in embed_str
        ]
    )
    chunk_input_ids = chunk_tensors(encoded_input, max_tokens, overlap_window)
    chunk_input_strings = [tokenizer.decode(id) for id in chunk_input_ids.tolist()]

    embeddings, usage = [], 0
    for i in range(0, len(chunk_input_strings), 128):
        batch_strings = chunk_input_strings[i : i + 128]
        response = await client.embed(
            batch_strings, input_type="query", model=model_name
        )
        embeddings.extend(response.embeddings)
        usage += response.total_tokens

    # return mean across chunks
    embeddings = torch.tensor(embeddings)
    num_chunks = int(chunk_input_ids.shape[0] / encoded_input.shape[0])
    mean_embeddings = torch.mean(
        embeddings.view(num_chunks, encoded_input.shape[0], -1), dim=0
    )
    return mean_embeddings, usage


def sliding_chunking(
    input_tensor: torch.Tensor, chunk_size: int, overlap_size: int, padding_value=0
) -> torch.Tensor:
    """crop sequences to chunk_size length, each sequence overlaps by overlap_size"""
    pad_dim = overlap_size - (input_tensor.size(1) % overlap_size)
    input_tensor = (
        torch.nn.functional.pad(input_tensor, (0, pad_dim), value=padding_value)
        if pad_dim > 0
        else input_tensor
    )
    # Unfold the input tensor with the specified chunk and overlap sizes
    unfolded_tensor = input_tensor.unfold(1, chunk_size, chunk_size - overlap_size)
    chunks = torch.chunk(unfolded_tensor, chunks=unfolded_tensor.shape[1], dim=1)
    return torch.cat(chunks, dim=0).squeeze(dim=1)  # B * (idk) x C


def batched_chunking(
    input_tensor: torch.Tensor, chunk_size: int, padding_value=0
) -> torch.Tensor:
    """naively crop sequences to the chunk_size length, batch resulting chunks"""
    # pad with 0s if necessary
    pad_dim = chunk_size - (input_tensor.size(1) % chunk_size)
    input_tensor = (
        torch.nn.functional.pad(input_tensor, (0, pad_dim), value=padding_value)
        if pad_dim > 0
        else input_tensor
    )
    chunks = torch.split(input_tensor, chunk_size, dim=1)  # B x T -> Tuple[BxC]
    output_tensor = torch.cat(chunks, dim=0)  # B*T/C x C
    return output_tensor


def chunk_tensors(
    tokens: List[int], chunk_size: int, overlap: int = None
) -> Tuple[torch.Tensor, int]:
    """route chunking to sliding window or batched"""
    if chunk_size > tokens.shape[1]:
        return tokens
    if overlap:
        return sliding_chunking(tokens, chunk_size, overlap)
    else:
        return batched_chunking(tokens, chunk_size)


def embed_text(
    embed_str: List[str],
    model_name: str = "flag",
    model: str = "BAAI/bge-small-en-v1.5",
    max_tokens: int = 512,
    overlap_window: Optional[int] = None,
    batch_size: int = 10,
    show_progress: bool = True,
    **kwargs,
) -> List[torch.Tensor]:
    if model_mapping[model].org == "openai":
        client, tokenizer, max_tokens = setup_ada_normal(model)
        tensors, usage = run_ada_normal(
            client, model, tokenizer, embed_str, max_tokens, overlap_window
        )
    elif model_mapping[model].org == "voyage":
        client, tokenizer, max_tokens = setup_voyage(model)
        tensors, usage = asyncio.run(
            run_voyage(client, model, tokenizer, embed_str, max_tokens, overlap_window)
        )
        list_of_floats = [t.tolist() for t in tensors]
        return list_of_floats, usage
    else:
        model_nn, tokenizer, max_tokens = setup_llm_embedder(model)
        tensors, usage = run_llm_embedder(
            model_nn,
            tokenizer,
            embed_str,
            max_tokens,
            overlap_window,
            batch_size,
            show_progress=show_progress,
            task=kwargs.get("task", "icl"),
        )

    list_of_floats = [t.tolist() for t in tensors]
    return list_of_floats


async def aembed_text(
    embed_str: List[str],
    model: str = "voyage-law-2",
    max_tokens: int = 350,
    overlap_window: Optional[int] = None,
    batch_size: int = 10,
    **kwargs,
) -> Tuple[List[List[float]], float]:
    if model_mapping[model].org == "voyage":
        client, tokenizer, max_tokens = setup_voyage(model)
        tensors, usage = await run_voyage(
            client, model, tokenizer, embed_str, max_tokens, overlap_window
        )
        embeddings = [t.tolist() for t in tensors]
        return embeddings, usage
