"""
Comparison functions
"""

from typing import Any


def cmp(left: Any, right: Any) -> int:
    """
    We no longer have this function in python3, so duplicate its functionality

    Args:
        left (Any): left param
        right (Any): right param

    Returns:
        int: -1 if left < right, 0 if left == right, 1 if left > right
    """
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


def cmp_len_then_content(left: Any, right: Any) -> int:
    """
    Comparison where string length counts first, then content for same-length items

    Args:
        left (Any): left param
        right (Any): right param

    Returns:
        int: -1 if left < right, 0 if left == right, 1 if left > right
    """
    return cmp(len(left), len(right)) or cmp(left, right)
