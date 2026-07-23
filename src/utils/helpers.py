"""
Tiny, generic utility functions that don't belong to any one module.
"""


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def truncate(text: str, max_length: int = 60) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
