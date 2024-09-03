import os

from ..algorithms.levenshtein import levenshtein

_cached_distance = {}


def _distance(a, b):
    if b < a:
        a, b = b, a
    key = (a, b)
    if key not in _cached_distance:
        _cached_distance[key] = levenshtein(
            a, b, keyfn=lambda x: os.path.splitext(x)[0])
    return _cached_distance[key]


def partition_filenames(dn):
    fns = sorted([fn for fn in os.listdir(
        dn) if os.path.isfile(os.path.join(dn, fn))])
    l = len(fns)
    for i in range(l - 1):
        for j in range(i + 1, l):
            print(f'{fns[i]} / {fns[j]} / {_distance(fns[i], fns[j])}')


if __name__ == '__main__':
    partition_filenames('/Users/greeng3/Dropbox/files')
