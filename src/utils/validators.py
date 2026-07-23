"""
Small, pure "is this valid?" checks. No side effects, no printing.
"""


def is_valid_task_index(index_str: str, queue_length: int) -> bool:
    try:
        index = int(index_str) - 1
    except ValueError:
        return False
    return 0 <= index < queue_length


def parse_priority(raw_input: str, default: int = 2) -> int:
    normalized = raw_input.strip().lower()
    if normalized in ('1', 'h', 'high'):
        return 1
    if normalized in ('3', 'l', 'low'):
        return 3
    return default


def is_valid_url(action: str) -> bool:
    return action.startswith('http://') or action.startswith('https://')
