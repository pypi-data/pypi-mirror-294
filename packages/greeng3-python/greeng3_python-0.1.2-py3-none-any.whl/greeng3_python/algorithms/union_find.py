# The point of this is to implement an integer-based WQUPC union-find implementation along the lines of the one in
# 01UnionFind.pdf, which appear to be lecture notes to some Algorithms in Java class.


class WQUPC:
    def __init__(self, initial_size=0):
        self._id = range(initial_size)
        self._size = [1] * initial_size

    def add(self):
        n = len(self._id)
        self._id.append(n)
        self._size.append(1)
        return n

    def equivalent(self, p, q):
        return self.find(p) == self.find(q)

    def find(self, p):
        if p == self._id[p]:
            return p
        else:
            self._id[p] = self.find(self._id[p])
            return self._id[p]

    def union(self, p, q):
        i = self.find(p)
        j = self.find(q)
        if i == j:
            # already connected
            return
        if self._size[i] < self._size[j]:
            self._id[i] = j
            self._size[j] += self._size[i]
        else:
            self._id[j] = i
            self._size[i] += self._size[j]


if __name__ == '__main__':
    wqupc = WQUPC()
    print(wqupc._id, wqupc._size)
    print(wqupc.add(), wqupc._id, wqupc._size)
    print(wqupc.add(), wqupc._id, wqupc._size)
    print(wqupc.add(), wqupc._id, wqupc._size)
