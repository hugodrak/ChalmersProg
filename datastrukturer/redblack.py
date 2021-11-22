class Node:
    """A node in a red-black tree."""

    def __init__(self, is_red, key, value, left=None, right=None):
        self._is_red = is_red
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def is_red(self):
        if self is None:
            return False
        else:
            return self._is_red

    def is_black(self):
        return not Node.is_red(self)

    def __str__(self):
        return "Node(%s, %s, %s, %s, %s)" % \
               (self._is_red, self.key, self.value, self.left, self.right)


class RedBlackTree:
    """A dictionary implemented using a binary search tree."""

    def __init__(self):
        self.root = None

    def check_invariant(self):
        """Check that the invariant holds."""

        if Node.is_red(self.root):
            raise AssertionError("red root")

        self.check_invariant_helper(self.root, None, None)

    @staticmethod
    def check_invariant_helper(node, lo, hi):
        """Helper method for 'check_invariant'.

        Checks that the node is the root of a valid red-black tree, and that
        all keys k satisfy lo < k < hi. The test lo < k is skipped
        if lo is None, and k < hi is skipped if hi is None.

        Returns the "black height" of the tree."""

        if node is None: return 0

        if Node.is_red(node.right):
            raise AssertionError("red right child")

        if Node.is_red(node) and Node.is_red(node.left):
            raise AssertionError("red node with red left child")

        if lo is not None and node.key <= lo:
            raise AssertionError("key too small", node.key, lo, hi)

        if hi is not None and node.key >= hi:
            raise AssertionError("key too big", node.key, lo, hi)

        # Keys in the left subtree should be < node.key
        h1 = RedBlackTree.check_invariant_helper(node.left, lo, node.key)
        # Keys in the right subtree should be > node.key
        h2 = RedBlackTree.check_invariant_helper(node.right, node.key, hi)

        if h1 != h2:
            raise AssertionError("unbalanced tree")

        return h1 + (1 if Node.is_black(node) else 0)

    def isEmpty(self):
        """Return true if there are no keys."""

        return self.root is not None

    def size(self):
        """Return the number of keys."""

        return self.size_helper(self.root)

    @staticmethod
    def size_helper(node):
        """Helper method for 'size'."""

        if node is None:
            return 0
        else:
            return 1 + size_helper(node.left) + size_helper(node.right)

    def containsKey(self, key):
        """Return true if the key has an associated value."""

        return self.get(key) is not None

    def get(self, key):
        """Look up a key."""

        return self.get_helper(self.root, key)

    @staticmethod
    def get_helper(node, key):
        """Helper method for 'get'."""

        if node is None:
            return None
        elif key < node.key:
            return RedBlackTree.get_helper(node.left, key)
        elif key > node.key:
            return RedBlackTree.get_helper(node.right, key)
        else:
            return node.value

    def put(self, key, value):
        """Add a key-value pair, or update the value associated with
        an existing key.

        Returns the value previously associated with the key, or None
        if the key was not present."""

        self.root, old_value = self.put_helper(self.root, key, value)
        if Node.is_red(self.root):
            self.root._is_red = False
        return old_value

    @staticmethod
    def put_helper(node, key, value):
        """Helper method for 'put'.

        Returns the updated node, and the value previously associated
        with the key."""

        if node is None:
            return Node(True, key, value, None, None), None
        elif key < node.key:
            node.left, old_value = RedBlackTree.put_helper(node.left, key, value)
        elif key > node.key:
            node.right, old_value = RedBlackTree.put_helper(node.right, key, value)
        else:
            old_value = node.value
            node.value = value
        return RedBlackTree.rebalance(node), old_value

    @staticmethod
    def rebalance(node):
        if node is None: return None

        # Skew
        if Node.is_red(node.right):
            node = RedBlackTree.rotate_left(node)

        # Split part 1
        if Node.is_red(node.left) and Node.is_red(node.left.left):
            node = RedBlackTree.rotate_right(node)

        # Split part 2
        if Node.is_red(node.left) and Node.is_red(node.right):
            node.left._is_red = False
            node.right._is_red = False
            node._is_red = True

        return node

    @staticmethod
    def rotate_left(node):
        """
        Left rotation.

           x                y
          / \              / \
         A  y      ===>   x  C
           / \           / \
          B  C          A  B
        """

        # Variables are named according to the picture above.
        x = node
        A = x.left
        y = x.right
        B = y.left
        C = y.right

        # We also swap x's and y's colours
        # (e.g. if x was black before, then y will be black afterwards).
        return Node(is_red=x.is_red(), key=y.key, value=y.value,
                    left=
                    Node(is_red=y.is_red(), key=x.key, value=x.value,
                         left=A, right=B),
                    right=C)

    @staticmethod
    def rotate_right(node):
        """
        Right rotation.

             x             y
            / \           / \
           y  C    ===>  A  x
          / \              / \
         A  B             B  C
        """

        # Variables are named according to the picture above.
        x = node
        y = x.left
        A = y.left
        B = y.right
        C = x.right

        # We also swap x's and y's colours
        # (e.g. if x was black before, then y will be black afterwards).
        return Node(is_red=x.is_red(), key=y.key, value=y.value,
                    left=A,
                    right=
                    Node(is_red=y.is_red(), key=x.key, value=x.value,
                         left=B, right=C))

    def __iter__(self):
        """Iterate through all keys.

        This is called when the user writes 'for key in bst: ...'."""

        return self.iter_helper(self.root)

    @staticmethod
    def iter_helper(node):
        """Helper method for '__iter__'."""

        # This method is a generator:
        # https://docs.python.org/3/howto/functional.html#generators
        # Generators are an easy way to make iterators

        if node is None:
            return
        else:
            for key in RedBlackTree.iter_helper(node.left):
                yield key
            yield node.key
            for key in RedBlackTree.iter_helper(node.right):
                yield key

    def __getitem__(self, key):
        """This is called when the user writes 'x = bst[key]'."""

        return self.get(key)

    def __setitem__(self, key, value):
        """This is called when the user writes 'bst[key] = value'."""

        self.put(key, value)

    def __delitem__(self, key):
        """This is called when the user writes 'del bst[key]'."""

        self.remove(key)

    def __str__(self):
        """This is called to show the red-black tree as a string."""

        # Use a dict comprehension to convert the red-black tree into a dict:
        # https://docs.python.org/3/tutorial/datastructures.html#dictionaries
        # Then show the dict as a string.

        return str({key: self[key] for key in self})
        # This code is the same as:
        # d = {}
        # for key in self:
        #   d[key] = self[key]
        # return str(d)
        # Note that 'for key in self' calls self.__iter__ to produce
        # the keys, and 'self[key]' calls self.__getitem__.

    def __repr__(self):
        """This is called to show the red-black tree as a string."""

        return repr({key: self[key] for key in self})


# Some code to test that the tree is working
if __name__ == '__main__':
    bst = RedBlackTree()
    keys = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6]
    values = list(range(len(keys)))

    for i in range(len(keys)):
        bst[keys[i]] = values[i]
        print(bst.root)
        bst.check_invariant()
    for i in range(len(keys)):
        print(bst[keys[i]])
        bst.check_invariant()