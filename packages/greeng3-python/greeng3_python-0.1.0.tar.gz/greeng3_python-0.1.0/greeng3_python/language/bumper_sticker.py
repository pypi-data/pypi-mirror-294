"""
Spell things with bumper stickers
"""

from collections import defaultdict
from typing import Dict, Tuple


def take_inventory(msg: str) -> Dict[str, int]:
    """
    Count the occurrences of letters in msg and return the counts as a dict

    Args:
        msg (str): bumper sticker or message

    Returns:
        dict: counts of letters occurring in msg
    """
    inventory: Dict[str, int] = defaultdict(int)

    for char in msg.lower():
        if char in 'abcdefghijklmnopqrstuvwxyz':
            inventory[char] += 1

    return inventory


def spell_it(msg: str, sticker: str) -> Tuple[bool, int]:
    """
    Figure out how many of a given bumper sticker it takes to spell a message (if possible)

    Args:
        msg (str): the message you want to spell
        sticker (str): the bumper sticker text

    Returns:
        Tuple[bool, int] - True if we could spell it, and how many sticker we need, or False if we couldn't
    """
    msg_inventory = take_inventory(msg)
    sticker_inventory = take_inventory(sticker)

    max_stickers = 0

    for k, v in msg_inventory.items():
        if k not in sticker_inventory:
            return False, 0
        need = (v + sticker_inventory[k] - 1) / sticker_inventory[k]
        max_stickers = max(max_stickers, need)

    return True, max_stickers


if __name__ == '__main__':
    sticker = 'Rensselaer Polytechnic Institute'

    msg = 'pneumonoultramicroscopicsilicovolcanoconiosis'
    print(f'{msg}: {spell_it(msg, sticker)}')

    msg = 'resistor potential intrinsic'
    print(f'{msg}: {spell_it(msg, sticker)}')
