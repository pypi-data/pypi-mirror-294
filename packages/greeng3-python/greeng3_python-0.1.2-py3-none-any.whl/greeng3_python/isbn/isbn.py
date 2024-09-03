"""
ISBN: https://en.wikipedia.org/wiki/ISBN

ISSN: https://en.wikipedia.org/wiki/International_Standard_Serial_Number
"""

import re

ISBN_RE = re.compile(
    '[Ii][Ss][Bb][Nn](?:-1[03])?:?\s*(\d((\s|-)*\d){8,11}(\s|-)*(\d|[Xx]))')
RAW_RE = re.compile('(\d((\s|-)*\d){8,11}(\s|-)*(\d|[Xx]))')
DIGIT_VALUES = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'X': 11, 'x': 11,
}


def _to_values(s):
    """
    Extraact the numbers from an ISBN string
    :param s: a string containing digits, maybe separated by spaces and hyphens, and maybe X or x as a check digit
    :return: a list of numbers corresponding to those digits and a string of the actual digits
    """
    values, digits = [], []
    for c in s:
        if c in DIGIT_VALUES:
            values.append(DIGIT_VALUES[c])
            digits.append(c)
    return values, ''.join(digits)


def _isbn_is_valid_10(numbers):
    """
    Check a 10-digit ISBN

    :param numbers: list of the numeric values of all digits
    :return: True if valid, False otherwise
    """
    s, t = 0, 0
    for i in range(10):
        t += numbers[i]
        s += t
    return (s % 11) == 0


def _isbn_is_valid_13(numbers):
    """
    Check a 13-digit ISBN

    :param numbers: list of the numeric values of all digits
    :return: True if valid, False otherwise
    """
    accum = 0
    for i in range(13):
        multiplier = 1 + 2 * (i % 2)
        accum += numbers[i] * multiplier
    return (accum % 10) == 0


def isbn_is_valid(numbers):
    """
    Check a 10- or 13-digit ISBN

    :param numbers: list of the numeric values of all digits
    :return: True if valid, False otherwise
    """
    ln = len(numbers)
    if ln == 10:
        return _isbn_is_valid_10(numbers)
    elif ln == 13:
        return _isbn_is_valid_13(numbers)
    return False


def _isbn_find(m):
    """
    Given a match object to an ISBN regex, process the ISBN it matched

    :param m: a match object from an ISBN regex
    :return: string of the compacted ISBN digits, or an empty string if no ISBN-like substance were found
    """
    if m:
        numbers, digits = _to_values(m.group(1))
        if isbn_is_valid(numbers):
            return digits
    return ''


def isbn_find(text):
    """
    Given a block of text, find an ISBN in it

    :param text: block of text to search
    :return: string of the compacted ISBN digits, or an empty string if no ISBN-like substance were found
    """
    m = ISBN_RE.search(text)
    return _isbn_find(m) if m else ''""''


def isbn_find_raw(text):
    """
    Given a block of text, find a raw ISBN in it

    :param text: block of text to search
    :return: string of the compacted ISBN digits, or an empty string if no ISBN-like substance were found
    """
    m = RAW_RE.search(text)
    return _isbn_find(m) if m else ''""''


def cmp(l, r):
    """
    We no longer have this function in python3, so duplicate its functionality

    Args:
        l (Any):  left param
        r (Any):  right param
    """
    if l < r:
        return -1
    if l > r:
        return 1
    return 0


def isbn_cmp(l, r):
    """
    :param l: str: left param
    :param r: str: right param
    :return: int: Comparison of ISBNs, preferring the longer and larger of the two.
    """
    return cmp(len(r), len(l)) or cmp(r, l)


if __name__ == '__main__':
    def test(s):
        print(f'{s}:')
        print('    {isbn_find(s)}')

    def test_raw(s):
        print('{s}:')
        print('    {isbn_find_raw(s)}')

    test('ISBN-13: 978-1-4028-9462-6')
    test('ISBN-13: 9781402894626')
    test('ISBN-10: 0-596-00681-0')
    test('ISBN-10: 0596006810')
    test('ISBN: 978-1-4028-9462-6')
    test('ISBN: 0-596-00681-0')
    test('0-596-00681-0')
    test_raw('0-596-00681-0')
    test_raw('978-0-12-800631-3')
    test_raw('Time and Relational Theory, (2014). 978-0-12-800631-3')
