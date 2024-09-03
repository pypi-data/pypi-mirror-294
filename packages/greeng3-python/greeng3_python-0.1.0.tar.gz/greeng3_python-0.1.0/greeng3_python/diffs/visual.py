"""
Utilities for performing diffs
"""
from difflib import ndiff
from typing import Dict, List, Tuple


def string_diff_visual_aid(from_str: str, to_str: str):
    """
    Display a visual diff between two strings along the same general principle as the unix diff utility.
    In this case, we are comparing characters rather than lines, but the output makes it easier to pick
    out the differences between two long and similar strings (such as urls with long parameter strings).

    Args:
        from_str (str): the "from" string
        to_str (str): the "from" string

    Returns: 
        Tuple[str, str, str]: a 3-tuple containing strings suitable for printing one after another at the same indent
             first entry is the "from" string, possibly stretched where changes were
             second entry is a string of spaces and pipes, where pipes indicate changes between the strings
             third entry is the "to" string, possibly stretched where changes where
    """
    state: Dict[str, List[str]] = {
        'out1': [],
        'between': [],
        'out2': [],
        'deleted': [],
        'added': [],
    }

    def reconcile_differences(state_dict: Dict[str, List[str]]):
        """
        This takes a (possibly empty) string of deleted characters and a (possibly empty) string of added
        characters, padding them to be the same length and providing the right number of pipes for visual
        ease when displayed.

        Args:
            state_dict (_type_): _description_
        """
        len_deleted = len(state_dict['deleted'])
        len_added = len(state_dict['added'])
        max_len = max(len_deleted, len_added)
        if max_len:
            state_dict['out1'] += state_dict['deleted'] + \
                [' '] * (max_len - len_deleted)
            state_dict['out2'] += state_dict['added'] + \
                [' '] * (max_len - len_added)
            state_dict['between'] += ['|'] * max_len
            state_dict['deleted'] = []
            state_dict['added'] = []

    # this mess interprets the output of ndiff and builds up strings from unchanged, deleted, and added parts,
    # adding spaces where the changes aren't the same length, and adding pipes in the between string to
    # make it visually easier to spot the differences
    for index, string in enumerate(ndiff(from_str, to_str)):
        if string[0] == ' ':
            reconcile_differences(state)
            state['out1'].append(string[-1])
            state['between'].append(' ')
            state['out2'].append(string[-1])
        elif string[0] == '-':
            state['deleted'].append(string[-1])
        elif string[0] == '+':
            state['added'].append(string[-1])
        else:
            print(index, string)
    reconcile_differences(state)
    return ''.join(state['out1']), ''.join(state['between']), ''.join(state['out2'])


def example_string_diff_visual_aid(from_str: str, to_str: str, chunk_size: int = 80):
    """
    Example for use of string_diff_visual_aid().
    It just calls that with the same parameters and prints what it returns in the manner intended.

    Args:
        from_str (str): the "from" string
        to_str (str): the "from" string
        chunk_size (int): break lines into chunks of this size so word wrap doesn't make the output confusing
    """
    from_out, between, to_out = string_diff_visual_aid(from_str, to_str)

    # all these values should be of the same length, as they'll have been padded
    while len(from_out) > 0:
        print(from_out[:chunk_size])
        print(between[:chunk_size])
        print(to_out[:chunk_size])
        if len(from_out) > chunk_size:
            print('-' * chunk_size)

        from_out = from_out[chunk_size:]
        between = between[chunk_size:]
        to_out = to_out[chunk_size:]
