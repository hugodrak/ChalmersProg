from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class LinkedListNode:
    key: Any
    value: Any
    next: Optional[LinkedListNode] = None


class LinkedListMap:
    def __init__(self):
        self.first: Optional[LinkedListNode] = None

    def iter_nodes(self):

        node = self.first
        while node is not None:
            yield node
            node = node.next

    def set(self, key, value):
        if self.first is None:
            self.first = LinkedListNode(key, value)
            return

        for node in self.iter_nodes():
            if node.key == key:
                node.value = value
                return

        node.next = LinkedListNode(key, value)

    def contains_key(self, key) -> bool:
        if self.first is None:
            return False

        for node in self.iter_nodes():
            if node.key == key:
                return True

        return False

    def get(self, key) -> Optional[Any]:
        if self.first is None:
            return None

        for node in self.iter_nodes():
            if node.key == key:
                return node.value

        return None

    def __str__(self):
        return '[' + ', '.join(f'({node.key}:{node.value})' for node in self.iter_nodes()) + ']'


class Bucket(LinkedListMap):
    pass


class HashMap:

    def __init__(self, size=4):
        self.num_items = 0
        self._current_size = size
        self._buckets = [Bucket() for _ in range(size)]

    @property
    def bucket_size(self):
        return len(self._buckets)

    def hash_function(self, key) -> int:
        return (11 * ord(key)) % self.bucket_size

    def set(self, key, value):
        bucket = self._buckets[self.hash_function(key)]
        bucket.set(key, value)
        self.num_items += 1

    def get(self, key) -> Optional[Any]:
        bucket = self._buckets[self.hash_function(key)]
        return bucket.get(key)

    def print(self):
        for index, b in enumerate(self._buckets):
            print(index, str(b))


if __name__ == '__main__':
    m = HashMap()

    d = "easyqution"

    for c in d:
        m.set(c, ord(c))

    m.print()

    for c in d:
        print(c, chr(m.get(c)))
