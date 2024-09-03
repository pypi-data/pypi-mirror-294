from difflib import ndiff


def string_diff_visual_aid(str1, str2):
    """
    Moved to python_library

    Display a visual diff between two strings along the same general principle as the unix diff utility.
    In this case, we are comparing characters rather than lines, but the output makes it easier to pick
    out the differences between two long and similar strings (such as urls with long parameter strings).

    :param str1: string - the "from" string
    :param str2: string - the "to" string
    :return: a 3-tuple containing strings suitable for printing one after another at the same indent
             first entry is the "from" string, possibly stretched where changes were
             second entry is a string of spaces and pipes, where pipes indicate changes between the strings
             third entry is the "to" string, possibly stretched where changes where
    """
    state = {
        'out1': [],
        'between': [],
        'out2': [],
        'deleted': [],
        'added': [],
    }

    # This takes a (possibly empty) string of deleted characters and a (possibly empty) string of added
    # characters, padding them to be the same length and providing the right number of pipes for visual
    # ease when displayed.
    def reconcile_differences(state_dict):
        ld, la = len(state_dict['deleted']), len(state_dict['added'])
        mlen = max(ld, la)
        if mlen:
            state_dict['out1'] += state_dict['deleted'] + [' '] * (mlen - ld)
            state_dict['out2'] += state_dict['added'] + [' '] * (mlen - la)
            state_dict['between'] += ['|'] * mlen
            state_dict['deleted'] = []
            state_dict['added'] = []

    # this mess interprets the output of ndiff and builds up strings from unchanged, deleted, and added parts,
    # adding spaces where the changes aren't the same length, and adding pipes in the between string to
    # make it visually easier to spot the differences
    for i, s in enumerate(ndiff(str1, str2)):
        if s[0] == ' ':
            reconcile_differences(state)
            state['out1'].append(s[-1])
            state['between'].append(' ')
            state['out2'].append(s[-1])
        elif s[0] == '-':
            state['deleted'].append(s[-1])
        elif s[0] == '+':
            state['added'].append(s[-1])
        else:
            print i, s
    reconcile_differences(state)
    return ''.join(state['out1']), ''.join(state['between']), ''.join(state['out2'])


def test_string_diff_visual_aid(str1, str2, chunk_size=80):
    """
    Moved to python_library

    Test (or the actually useful call to) string_diff_visual_aid().
    It just calls that with the same parameters and prints what it returns in the manner intended.

    :param str1: string - the "from" string
    :param str2: string - the "to" string
    :param chunk_size: int - break lines into chunks of this size so word wrap doesn't make the output confusing
    """
    out1, between, out2 = string_diff_visual_aid(str1, str2)

    # all these values should be of the same length, as they'll have been padded
    while len(out1) > 0:
        print(out1[:chunk_size])
        print(between[:chunk_size])
        print(out2[:chunk_size])
        if len(out1) > chunk_size:
            print('-' * chunk_size)

        out1 = out1[chunk_size:]
        between = between[chunk_size:]
        out2 = out2[chunk_size:]
