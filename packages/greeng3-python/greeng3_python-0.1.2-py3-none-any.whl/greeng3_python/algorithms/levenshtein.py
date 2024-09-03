def levenshtein(a, b, keyfn=lambda x: x):
    """
    Calculates the Levenshtein (edit) distance between a and b.
    :param a: one string
    :param b: the other string
    :param keyfn: optional key extraction function
    :return: int - the edit distancew
    """

    # Make sure n <= m, to use O(min(n,m)) space
    n, m = len(a), len(b)
    if n > m:
        a, b, n, m = b, a, m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if keyfn(a[j - 1]) != keyfn(b[i - 1]):
                change += 1
            current[j] = min(add, delete, change)

    return current[n]
