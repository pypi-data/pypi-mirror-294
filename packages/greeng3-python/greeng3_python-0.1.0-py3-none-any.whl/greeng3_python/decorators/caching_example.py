# This code is from Expert Python Programming.

import hashlib
import pickle
import time

cache = {}


def is_obsolete(entry, duration):
    return time.time() - entry['time'] > duration


def compute_key(function, args, kw):
    key = pickle.dumps((function.func_name, args, kw))
    return hashlib.sha1(key).hexdigest()


def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args, **kw):
            key = compute_key(function, args, kw)

            # do we have it already?
            if key in cache and not is_obsolete(cache[key], duration):
                print('we got a winner')
                return cache[key]['value']

            # computing
            result = function(*args, **kw)

            # storing the result
            cache[key] = {
                'value': result,
                'time': time.time(),
            }
            return result

        return __memoize

    return _memoize


@memoize()
def very_very_very_complex_stuff(a, b):
    # imagine this is too expensive to do gratuitously
    return a + b
