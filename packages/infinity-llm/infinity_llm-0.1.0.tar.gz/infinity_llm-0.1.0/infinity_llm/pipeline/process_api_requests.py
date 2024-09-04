import json, logging, asyncio, time, aiohttp

from infinity_llm import model_mapping, Provider, Functionality
from .utils import (
    task_id_generator_function,
    APIRequest,
    StatusTracker,
    num_tokens_consumed_from_request,
)
from .api_requests import get_request_url, get_request_header


async def process_api_requests_from_file(
    requests_filepath: str,
    save_filepath: str,
    provider: Provider,
    functionality: Functionality,
    model: str,
    max_attempts: int = 5,
    logging_level: int = logging.INFO,
):
    # constants
    seconds_to_pause_after_rate_limit_error = 15
    seconds_to_sleep_each_loop = (
        0.001  # 1 ms limits max throughput to 1,000 requests per second
    )

    logging.basicConfig(level=logging_level)
    logging.debug(f"Logging initialized at level {logging_level}")

    # initialize trackers
    queue_of_requests_to_retry = asyncio.Queue()
    task_id_generator = task_id_generator_function()
    status_tracker = StatusTracker()
    next_request = None

    # initialize available capacity counts
    if provider == Provider.ANYSCALE:
        max_in_flight = model_mapping[model].limit.max_in_flight
    else:
        # mistral has no RPM rate limit, so use big number
        if provider == Provider.MISTRAL:
            max_requests_per_minute = 1000000000
        else:
            max_requests_per_minute = model_mapping[model].limit.rpm
        max_tokens_per_minute = model_mapping[model].limit.tpm
        available_request_capacity = max_requests_per_minute
        available_token_capacity = max_tokens_per_minute

    last_update_time = time.time()

    # initialize flags
    file_not_finished = True  # after file is empty, skip reading it
    logging.debug(f"Initialization complete.")

    # get request header and url
    request_header = get_request_header(provider)
    request_url = get_request_url(provider, functionality)

    # initialize file reading
    with open(requests_filepath) as file:
        requests = file.__iter__()
        logging.debug(f"File opened. Entering main loop")
        async with aiohttp.ClientSession() as session:
            while True:
                # get next request (if one is not already waiting for capacity)
                if next_request is None:
                    if not queue_of_requests_to_retry.empty():
                        next_request = queue_of_requests_to_retry.get_nowait()
                        logging.debug(
                            f"Retrying request {next_request.task_id}: {next_request}"
                        )
                    elif file_not_finished:
                        try:
                            # get new request
                            request_json = json.loads(next(requests))
                            next_request = APIRequest(
                                task_id=next(task_id_generator),
                                request_json=request_json,
                                token_consumption=num_tokens_consumed_from_request(
                                    request_json, request_url, provider=provider
                                ),
                                attempts_left=max_attempts,
                                metadata=request_json.pop("metadata", None),
                            )
                            status_tracker.num_tasks_started += 1
                            status_tracker.num_tasks_in_progress += 1
                            logging.debug(
                                f"Reading request {next_request.task_id}: {next_request}"
                            )
                        except StopIteration:
                            # if file runs out, set flag to stop reading it
                            logging.debug("Read file exhausted")
                            file_not_finished = False

                # update available capacity for rpm/tpm rate limiting
                if provider != Provider.ANYSCALE:
                    current_time = time.time()
                    seconds_since_update = current_time - last_update_time
                    available_request_capacity = min(
                        available_request_capacity
                        + max_requests_per_minute * seconds_since_update / 60.0,
                        max_requests_per_minute,
                    )
                    available_token_capacity = min(
                        available_token_capacity
                        + max_tokens_per_minute * seconds_since_update / 60.0,
                        max_tokens_per_minute,
                    )
                    last_update_time = current_time

                # if enough capacity available, call API
                can_process_request = False
                if next_request:
                    if provider == Provider.ANYSCALE:
                        can_process_request = (
                            status_tracker.num_tasks_in_process < max_in_flight
                        )
                    else:
                        next_request_tokens = next_request.token_consumption
                        can_process_request = (
                            available_request_capacity >= 1
                            and available_token_capacity >= next_request_tokens
                        )
                # update counters
                if can_process_request:
                    if provider != Provider.ANYSCALE:
                        available_request_capacity -= 1
                        available_token_capacity -= next_request_tokens
                    next_request.attempts_left -= 1

                    # call API
                    asyncio.create_task(
                        next_request.call_api(
                            session=session,
                            request_url=request_url,
                            request_header=request_header,
                            retry_queue=queue_of_requests_to_retry,
                            save_filepath=save_filepath,
                            status_tracker=status_tracker,
                        )
                    )
                    next_request = None  # reset next_request to empty

                # if all tasks are finished, break
                if status_tracker.num_tasks_in_progress == 0:
                    break

                # main loop sleeps briefly so concurrent tasks can run
                await asyncio.sleep(seconds_to_sleep_each_loop)

                # if a rate limit error was hit recently, pause to cool down
                if provider != Provider.ANYSCALE:
                    seconds_since_rate_limit_error = (
                        time.time() - status_tracker.time_of_last_rate_limit_error
                    )
                    if (
                        seconds_since_rate_limit_error
                        < seconds_to_pause_after_rate_limit_error
                    ):
                        remaining_seconds_to_pause = (
                            seconds_to_pause_after_rate_limit_error
                            - seconds_since_rate_limit_error
                        )
                        await asyncio.sleep(remaining_seconds_to_pause)
                        # ^e.g., if pause is 15 seconds and final limit was hit 5 seconds ago
                        logging.warn(
                            f"Pausing to cool down until {time.ctime(status_tracker.time_of_last_rate_limit_error + seconds_to_pause_after_rate_limit_error)}"
                        )

        # after finishing, log final status
        logging.info(
            f"""Parallel processing complete. Results saved to {save_filepath}"""
        )
        if status_tracker.num_tasks_failed > 0:
            logging.warning(
                f"{status_tracker.num_tasks_failed} / {status_tracker.num_tasks_started} requests failed. Errors logged to {save_filepath}."
            )
        if status_tracker.num_rate_limit_errors > 0:
            logging.warning(
                f"{status_tracker.num_rate_limit_errors} rate limit errors received. Consider running at a lower rate."
            )
