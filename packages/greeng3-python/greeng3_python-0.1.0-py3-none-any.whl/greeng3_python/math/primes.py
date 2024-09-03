import json
import os
from collections import defaultdict

from ..process.interprocess_lock import Lock

msgs = 0


def msg(m):
    print(m)
    if False:
        global msgs
        msgs += 1
        if msgs > 100:
            exit()


class PrimeMgr(object):
    def __init__(self):
        """
        Manage prime number operations, including keeping a cache of the primes we've found so far.
        """
        here = os.path.dirname(__file__)
        self._prime_pn = os.path.join(here, 'primes.json')
        self._lock = Lock(
            '/tmp/primes_4E4CCE4A-6A61-4AF0-994A-F50CDB593D17.lock')
        self._max, self._primes = 2, [2]

    def __enter__(self):
        self._max, self._primes = self._get_primes()
        return self

    def __exit__(self, _type, value, traceback):
        self._save_primes()

    def _get_primes(self):
        """
        :return: max_prime, primes - where max_prime is the largest prime we have in our list, primes
                 If primes is empty, max_prime is 0
        """
        self._lock.acquire()
        try:
            with open(self._prime_pn, 'r') as fh:
                prime_dict = json.load(fh)
                max_prime = prime_dict['max_prime']
                primes = prime_dict['primes']
        except Exception as e:
            print(f'Failed to get saved primes: {e}')
            max_prime = 7
            primes = [2, 3, 5, 7]
        self._lock.release()
        return max_prime, primes

    def _save_primes(self):
        max_prime, primes = self._get_primes()
        if max_prime < self._max:
            self._lock.acquire()
            prime_dict = {
                'max_prime': self._max,
                'primes': self._primes,
            }
            try:
                with open(self._prime_pn, 'w') as fh:
                    json.dump(prime_dict, fh)
            except Exception as e:
                print(f'Failed to save primes: {e}')
            self._lock.release()

    def factorize(self, n):
        results = defaultdict(lambda: 0)
        prime_index = 0
        while n > 1:
            if prime_index >= len(self._primes):
                msg(f'Ran out of primes at index: {prime_index}')
                # add a new prime - start looking right after the max one we have, going by 2 to save work
                p = self._max + 2
                satisfied = False
                while not satisfied:
                    msg('Considering for prime: {p}')
                    for d in self._primes:
                        if d * d > p:
                            satisfied = True
                        elif p % d == 0:
                            break
                    # we won't fall off the end, one way or the other

                    if satisfied:
                        self._max = p
                        self._primes.append(p)
                        msg(f'New prime: {p}')
                    else:
                        p += 2
            else:
                p = self._primes[prime_index]
                if p * p > n:
                    results[n] += 1
                    msg(f'New factor: {n}, leaving 1')
                    n = 1
                elif n % p == 0:
                    results[p] += 1
                    n /= p
                    msg(f'New factor: {p}, leaving {n}')
                else:
                    prime_index += 1
        return results


if __name__ == '__main__':
    with PrimeMgr() as prime_mgr:
        prime_mgr.factorize(292)
    print('Done.')
