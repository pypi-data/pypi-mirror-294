"""
Uses of Zeller's Congruence to find what day of the week a date falls on.
"""


def day_of_week(year: int, month: int, day: int):
    """
    Find the 0-indexed (0 == Monday) day of the week the day falls on

    Args:
        year (int): the 4-digit year
        month (int): the month
        day (int): the day of the month

    Returns:
        int - 0-indexed day of the week via Zeller's Congruence
    """
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    year = year - 1 if month < 3 else year
    return (year + year // 4 - year // 100 + year // 400 + t[month - 1] + day) % 7
