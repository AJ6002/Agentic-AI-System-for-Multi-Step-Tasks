MAX_RETRIES = 3


def should_retry(current_retry: int) -> bool:
    return current_retry < MAX_RETRIES
