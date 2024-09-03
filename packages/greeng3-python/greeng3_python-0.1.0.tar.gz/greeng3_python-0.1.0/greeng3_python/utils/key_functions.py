"""
Key functions for use in sorting, etc.
"""

from typing import Any


def len_then_content(left: Any, right: Any) -> bool:
    """
    A key function which compares two items by length, and only then by content
    """
    len_left = len(left)
    len_right = len(right)

    if len_left < len_right:
        return True
    if len_left > len_right:
        return False
    return left < right
