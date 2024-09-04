import json, os, logging, aiohttp, asyncio, time
from dataclasses import dataclass, field
from .tokenize import get_chat_prompt_tokens, get_embed_input_tokens
from infinity_llm import Provider
from enum import Enum


class Functionality(Enum):
    CHAT = "chat"
    EMBEDDING = "embedding"


def task_id_generator_function():
    """Generate integers 0, 1, 2, and so on."""
    task_id = 0
    while True:
        yield task_id
        task_id += 1


def append_to_jsonl(data, filename: str, task_id) -> None:
    """Append a json payload to the end of a jsonl file."""
    json_string = json.dumps(data)
    save_file = f"{filename}/task_{task_id}.json"
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    with open(save_file, "a") as f:
        f.write(json_string + "\n")


def num_tokens_consumed_from_request(
    request_json: dict,
    api_endpoint: str,
    provider: Provider,
):
    """Count the number of tokens in the request. Only supports completion and embedding requests."""
    # chat completion tokens
    if (
        api_endpoint.endswith("chat/completions")
        or api_endpoint.endswith("chat")
        or api_endpoint.endswith("messages")
    ):
        # expected number of completion tokens
        max_tokens = request_json.get("max_tokens", 512)  # TODO
        n = request_json.get("n", 1)
        completion_tokens = n * max_tokens

        # prompt tokens
        num_tokens = len(get_chat_prompt_tokens(request_json, provider))
        return num_tokens + completion_tokens

    elif api_endpoint.endswith("embeddings") or api_endpoint.endswith("embed"):
        # embedding input tokens
        num_tokens = len(get_embed_input_tokens(request_json, provider))
        return num_tokens
    else:
        raise NotImplementedError(
            f'API endpoint "{api_endpoint}" not implemented in this script'
        )


@dataclass
class StatusTracker:
    """Stores metadata about the script's progress. Only one instance is created."""

    num_tasks_started: int = 0
    num_tasks_in_progress: int = 0  # script ends when this reaches 0
    num_tasks_succeeded: int = 0
    num_tasks_failed: int = 0
    num_rate_limit_errors: int = 0
    num_api_errors: int = 0  # excluding rate limit errors, counted above
    num_other_errors: int = 0
    time_of_last_rate_limit_error: int = 0  # used to cool off after hitting rate limits
    result_buffer: dict = field(
        default_factory=dict
    )  # Buffer for storing results temporarily
    next_expected_task_id: int = (
        0  # The next task ID expected to be written to the file
    )

    def write_buffered_results_in_order(self, save_filepath: str):
        """Write results from the buffer to the file in the order of task IDs."""
        while self.next_expected_task_id in self.result_buffer:
            data = self.result_buffer.pop(self.next_expected_task_id)
            append_to_jsonl(data, save_filepath, self.next_expected_task_id)  # NOTE
            self.next_expected_task_id += 1


@dataclass
class APIRequest:
    """Stores an API request's inputs, outputs, and other metadata. Contains a method to make an API call."""

    task_id: int
    request_json: dict
    token_consumption: int
    attempts_left: int
    metadata: dict
    result: list = field(default_factory=list)

    async def call_api(
        self,
        session: aiohttp.ClientSession,
        request_url: str,
        request_header: dict,
        retry_queue: asyncio.Queue,
        save_filepath: str,
        status_tracker: StatusTracker,
    ):
        """Calls the OpenAI API and saves results."""
        logging.info(f"Starting request #{self.task_id}")
        error = None
        try:
            async with session.post(
                url=request_url, headers=request_header, json=self.request_json
            ) as response:
                response = await response.json()
            if "error" in response:
                logging.warning(
                    f"Request {self.task_id} failed with error {response['error']}"
                )
                status_tracker.num_api_errors += 1
                error = response
                if "Rate limit" in response["error"].get("message", ""):
                    status_tracker.time_of_last_rate_limit_error = time.time()
                    status_tracker.num_rate_limit_errors += 1
                    status_tracker.num_api_errors -= (
                        1  # rate limit errors are counted separately
                    )

            # voyage rate limits don't throw errors, need to inspect response
            if request_url.split(".")[1] == "voyageai":
                if "detail" in response:
                    logging.warning(
                        f"Request {self.task_id} failed with error: RATE LIMIT"
                    )
                    status_tracker.num_api_errors += 1
                    error = response
                    if "rate limit" in response["detail"]:
                        status_tracker.time_of_last_rate_limit_error = time.time()
                        status_tracker.num_rate_limit_errors += 1
                        status_tracker.num_api_errors -= (
                            1  # rate limit errors are counted separately
                        )

        except Exception as e:  # catch naked exceptions
            logging.warning(f"Request {self.task_id} failed with Exception {e}")
            status_tracker.num_other_errors += 1
            error = e
        if error:
            self.result.append(error)
            if self.attempts_left:
                retry_queue.put_nowait(self)
            else:
                logging.error(
                    f"Request {self.request_json} failed after all attempts. Saving errors: {self.result}"
                )
                data = (
                    [self.request_json, [str(e) for e in self.result], self.metadata]
                    if self.metadata
                    else [self.request_json, [str(e) for e in self.result]]
                )
                # Add to buffer instead of writing directly
                status_tracker.result_buffer[self.task_id] = data
                status_tracker.num_tasks_in_progress -= 1
                status_tracker.num_tasks_failed += 1
        else:
            data = (
                [self.request_json, response, self.metadata]
                if self.metadata
                else [self.request_json, response]
            )
            # Add to buffer instead of writing directly
            status_tracker.result_buffer[self.task_id] = data
            status_tracker.num_tasks_in_progress -= 1
            status_tracker.num_tasks_succeeded += 1
            logging.debug(
                f"Request {self.task_id} buffered for writing to {save_filepath}"
            )

        # Attempt to write buffered results in order
        status_tracker.write_buffered_results_in_order(save_filepath)
