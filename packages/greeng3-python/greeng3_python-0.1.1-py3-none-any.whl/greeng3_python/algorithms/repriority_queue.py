"""
A prioty queue where we can queue objects under a key, and removing them in priorty order.
"""

from typing import Any, Callable, Dict, Optional


class RePriotyQueueObject:
    """
    Derive a class from this in order to put it onto a RePriorityQueue
    """

    def __init__(self, key: Any, priority: Any):
        """
        Minimum things needed are a hashable key, and a sortable priority

        Args:
            key (Any): a hashable key
            priority (Any): a sortable priority

        Raises:
            ValueError: neither key nor priority can be None
        """
        # ideally check if key is hashable
        if key is None:
            raise ValueError(f'key: {key} cannot be None')

        # ideally check whether priority is sortable
        if priority is None:
            raise ValueError(f'priority: {priority} cannot be None')

        self.key = key
        self.priority = priority
        self.slot = None


class RePriorityQueue:
    def __init__(self, cmp_fn: Callable):
        # number of items in the queue
        self._size: int = 0

        # the priority queue (1-indexed)
        self._pq: Dict = {}

        # items, indexed by key
        self._by_key: Dict = {}

        # the function used to compare the priorities of 2 items, notionally "<"
        # as in self._cmp_fn(item1.priority, item2.priority) ~ item1.priority < item2.priority
        self._cmp_fn: Callable = cmp_fn

    @property
    def size(self) -> int:
        return self._size

    @property
    def is_empty(self) -> bool:
        return self._size == 0

    def contains(self, key: Any) -> bool:
        return key in self._by_key

    def insert(self, item: RePriotyQueueObject) -> Optional(RePriotyQueueObject):
        """
        Insert a suitable object into the priority queue.

        If this is a duplicate key, it will supersede the previous value, which will be
        returned, else, None will be returned.

        Args:
            item (RePriotyQueueObject): the object to insert

        Returns:
            Optional(RePriotyQueueObject): old item at key, if there was one, None if a new key
        """
        if self.contains(item.key):
            old_item = self._by_key[item.key]
            slot = old_item.slot
            self._by_key[item.key] = item
            item.slot = slot
            self._pq[slot] = item
            if self._cmp_fn(item.priority, old_item.priority):
                self._swim(slot)
            else:
                self._sink(slot)
            return old_item

        self._size += 1
        self._pq[self._size] = item
        item.slot = self._size
        self._by_key[item.key] = item
        self._swim(self._size)
        return None

    def reprioritize_key(self, key: Any, new_priority: Any):
        """
        Change the priority of the item with this key.  If the new priority is the
        same as the old priority, this is a no-op.

        Args:
            key (Any): the key of the item to update
            new_priority (Any): the new priority

        Raises:
            IndexError: if the key is not in the queue
        """
        if not self.contains(key):
            raise IndexError(f'key: {key} is not in the queue')

        item = self._by_key(key)
        priority = item.priority
        if self._cmp_fn(new_priority, priority):
            self._swim(item.slot)
        elif self._cmp_fn(priority, new_priority):
            self._sink(item.slot)

    def delete_first(self) -> RePriotyQueueObject:
        """
        Delete the "first" item, the meaning of which is determine by the _cmp_fn.
        This would be equivalent to delete_min if _cmp_fn is "<", delete_max if _cmp_fn is ">",
        etc.

        Returns:
            RePriorityQueueObject: the removed item

        Raises:
            IndexError: if the queue is empty, there is nothing to return
        """
        if self.is_empty:
            raise IndexError(f'queue is empty')

        first_item = self._pq[1]
        self._exchange(1, self._size)
        self._size -= 1
        self._sink(1)
        del self._pq[self._size + 1]
        del self._by_key[first_item.key]
        return first_item

    def delete_key(self, key: Any) -> RePriotyQueueObject:
        """
        Delete the item with the given key,

        Returns:
            RePriorityQueueObject: the removed item

        Raises:
            IndexError: if the key is not in the queue
        """
        if not self.contains(key):
            raise IndexError(f'key: {key} is not in the queue')

        deleted_item = self._by_key[key]
        if deleted_item.slot != self._size:
            replacement_item = self._pq[self._size]
            self._exchange(deleted_item.slot, self._size)
            self.size -= 1
            if self._cmp_fn(deleted_item.priority, replacement_item.priority):
                self._sink(deleted_item.slot)
            elif self._cmp_fn(replacement_item.priority, deleted_item.priority):
                self._swim(deleted_item.slot)
        else:
            self.size -= 1
        del self._pq[self._size + 1]
        del self._by_key[key]
        return deleted_item

    def _exchange(self, a: int, b: int):
        """
        Exchange the items in slots a and b, upodating each item's slot.

        This does not sink or swim either of these, so it should only be called as part
        of larger operations in this class, and never from outside this class, directly.

        Args:
            a (int): one index
            b (int): the other index
        """
        item_a = self._pq[a]
        item_b = self._pq[b]
        self._pq[a] = item_b
        self._pq[b] = item_a
        item_a.slot = b
        item_b.slot = a

    def _swim(self, index: int):
        """
        Move an item at index towards the root, as far as it can go

        Args:
            index (int): index of the item to move
        """
        while index > 1 and self._cmp_fn(self._pq[index].priority, self._pq[index // 2].priority):
            self._exchange(index, index // 2)
            index = index // 2

    def _sink(self, index: int):
        """
        Move the item at index away from the root, as far as it needs to go

        Args:
            index (int): index of the item to move
        """
        while 2 * index <= self._size:
            parent = 2 * index
            if parent < self._size and self._cmp_fn(self._pq[parent + 1].priority, self._pq[parent].priority):
                parent += 1
            if self._cmp_fn(self._pq[parent].priority, self._pq[index].priority):
                break
            self._exchange(index, parent)
            index = parent
