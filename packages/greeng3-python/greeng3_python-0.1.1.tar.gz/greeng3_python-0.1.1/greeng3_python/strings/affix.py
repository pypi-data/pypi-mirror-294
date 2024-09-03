"""
Functions regarding string prefixes and suffixes
"""

from typing import Iterable


def any_prefix(prefixes: Iterable[str], string: str) -> bool:
    """
    Test whether string starts with any of the prefixes

    Args:
        prefixes (Iterable[str]): a collection of prefixes to check for
        string (str): the string to test for prefixes

    Returns:
        bool: True if string starts with any of the prefixes, False if not
    """
    return any(map(string.startswith, prefixes))


def any_suffix(suffixes: Iterable[str], string: str) -> bool:
    """
    Test whether string starts with any of the prefixes

    Args:
        suffixes (Iterable[str]): a collection of suffixes to check for
        string (str): the string to test for prefixes

    Returns:
        bool: True if string ends with any of the prefixes, False if not
    """
    return any(map(string.endswith, suffixes))
