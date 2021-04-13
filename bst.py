from __future__ import annotations
from typing import Optional, Any, List


class BinarySearchTree:

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty BST.
        """
        if root is None:
            self._root = None
            self.pokemon = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)  # self._left is an empty BST
            self._right = BinarySearchTree(None)  # self._right is an empty BST

    def is_empty(self) -> bool:
        """Return whether this BST is empty.
        """
        return self._root is None

    def insert(self, item: Any, pokemon: str) -> None:
        """Insert the given item into this tree.

        Do not change positions of any other values.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            # Make new leaf.
            # Note that self._left and self._right cannot be None when the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self.pokemon = pokemon
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left.insert(item, pokemon)
        else:
            self._right.insert(item, pokemon)

    def find_greater_or_equal_nodes(self, threshold: int) -> List[str]:
        lst = []

        if not self._left.is_empty() and self._left._root >= threshold :
            lst.extend(self._left.find_greater_or_equal_nodes(threshold))

        if self._root >= threshold:
            lst.extend([self.pokemon])

        if not self._right.is_empty():
            lst.extend(self._right.find_greater_or_equal_nodes(threshold))

        return lst
