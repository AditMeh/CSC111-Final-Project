"""
BST Module
===============================
The functions/classes defined in this class are responsible for representing a
a binary search tree and a few BST methods.

PLEASE NOTE: Some code in the binary search tree implementation
was pulled from the CSC111 course notes. I have modified that
implementation to fit my requirements and added my own functions.
===============================
This file is Copyright (c) 2021 Aditya Mehrotra.
"""

from __future__ import annotations
from typing import Optional, Any, List, Tuple


class BinarySearchTree:
    """
    A class that represents a BST

    Private Instance Attributes:
        - _root: The item stored in this tree, corresponds to
        a stat of a pokemon
        -  pokemon: The pokemon stored in this tree, where the stat
        comes from
        - _left: the left subtree
        - _right: the right subtree

        Representation Invariants:
        - self._left.root <= self._root <= self._right._root
        - self.pokemon != self._right.pokemon
        - self.pokemon != self._left.pokemon
    """
    def __init__(self, root: Optional[Any], pokemon: Optional[str]) -> None:
        """Initialize a new BST containing only the given root value
        and a pokemon.

        If <root> is None, initialize an empty BST.
        """
        if root is None:
            self._root = None
            self.pokemon = pokemon
            self._left = None
            self._right = None
        else:
            self._root = root
            self.pokemon = pokemon
            self._left = BinarySearchTree(None, None)  # self._left is an empty BST
            self._right = BinarySearchTree(None, None)  # self._right is an empty BST

    def is_empty(self) -> bool:
        """Return whether this BST is empty.
        """
        return self._root is None

    def insert(self, item: Any, pokemon: str) -> None:
        """Insert the given pokemon and stat
        from the pokemon nto this tree.

        Do not change positions of any other values.

        >>> bst = BinarySearchTree(10, pokemon="charmander")
        >>> bst.insert(3, "pikachu")
        >>> bst.insert(20, "charizard")
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        >>> bst.pokemon
        'charmander'
        >>> bst._left.pokemon
        'pikachu'
        >>> bst._right.pokemon
        'charizard'
        """
        if self.is_empty():

            self._root = item
            self.pokemon = pokemon
            self._left = BinarySearchTree(None, None)
            self._right = BinarySearchTree(None, None)
        elif item <= self._root:
            self._left.insert(item, pokemon)
        else:
            self._right.insert(item, pokemon)

    def find_greater_or_equal_nodes(self, threshold: Tuple[Optional[float], Optional[float]]) -> List[str]:
        """
        Given a threshold in the form of (Lower bound, Upper bound), this function finds
        all nodes in the BST which have values that are in between the upper and lower bounds
        (inclusive).

        However, in the case where there is no upper or lower bound, we have:
        -   (None, Upper bound) when there is no lower bound
        -   (Lower bound, None) when there is no upper bound

        In the first case, where there is no lower bound, we replace the lower bound with 0.
        Since each node has a pokemon stat value, we know all nodes will have a value greater
        than or equal to 0. Therefore, this function will return all nodes with
        a value that is less than or equal to the upper bound. Which is
        the desired effect in this case.

        In the second case, where there is no upper bound, we replace the upper
        bound with 500. Since eawch node has a pokemon stat value, we know all pokemon
        will have a stat value less than 500, this is because it isn't possible
        for a pokemon to have a stat of 500. Therefore, all nodes
        are less than 500. Hence, this function will return all nodes with
        a value that is greater than or equal to the lower bound. Which is
        the desired effect in this case.

        :param threshold:
            A tuple in the form (Lower bound, upper bound), where either can be none.
            The function's behavior when either are none is described above
        :return:
            A list of all pokemon names which have stat values that follow
            the constraints set out by the threshold tuple.
        """
        lst = []

        left_threshold = 0 if threshold[0] is None else threshold[0]
        right_threshold = 500 if threshold[1] is None else threshold[1]

        if not self._left.is_empty() and self._root >= left_threshold:
            lst.extend(self._left.find_greater_or_equal_nodes(threshold))

        if left_threshold <= self._root <= right_threshold:
            lst.extend([self.pokemon])

        if not self._right.is_empty() and self._root <= right_threshold:
            lst.extend(self._right.find_greater_or_equal_nodes(threshold))

        return lst
