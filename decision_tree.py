"""
Decision Tree Module
===============================
The functions/classes defined in this class are responsible for
representing a decision tree and the relevant methods
===============================
This file is Copyright (c) 2021 Aditya Mehrotra.
"""
from __future__ import annotations

from typing import Union, Optional, List, Dict
from bst import BinarySearchTree


class DecisionTree:
    """
    A class that represents a decision tree.


    Private Instance Attributes:
    - subtrees: A list of subtrees of the decision tree
    - category: The item that this decision tree represents
      for this project, the category can be a pokemon type or stat
    - _is_binary_parent: Whether this decision tree is a parent to a BST
    - conversion_dictionary: The dictionary used to convert the degree
      of a query into a numerical representation (see more in the project report)

    Representation invariants:
    - category in {'flying', 'ice', 'psychic', 'ghost', 'water', 'ground', 'steel',
    'rock', 'fighting', 'fire', 'electric', 'poison', 'grass', 'bug', 'dark', 'normal', 'fairy',
    'dragon', 'attack', 'defense', 'sp_attack', 'sp_defense', 'hp', 'speed}
    """
    subtrees: List[Union[BinarySearchTree, DecisionTree]]
    category: str
    _is_binary_parent: bool
    conversion_dictionary: Optional[Dict[str, tuple[Optional[float], Optional[float]]]]

    def __init__(self, category: Optional[str], is_binary_parent: bool,
                 conversion_dictionary: Optional[Dict[str, tuple[Optional[float], Optional[float]]]]) -> None:
        self.subtrees = []
        self.category = category
        self._is_binary_parent = is_binary_parent
        self.conversion_dictionary = conversion_dictionary

        # Tree can only have a query conversion dictionary if the subtree is a binary tree.
        assert conversion_dictionary is None or self._is_binary_parent

    def add_subtree(self, subtree: Union[BinarySearchTree, DecisionTree]) -> None:
        """
        Adds a subtree to this decision tree

        :param subtree:
            A BST or decision tree to add as a subtree to this decision tree
        """
        self.subtrees.append(subtree)

    def evaluate(self, query: List[str]) -> List[str]:
        """
        Evaluates this decision tree on a given query

        :param query:
            A list of strings, where each string is a keyword.
        :return:
            The result after evaluating the query
        """
        if not self._is_binary_parent:
            for item in self.subtrees:
                if item.category == query[0]:
                    return item.evaluate(query[1:])
        elif self._is_binary_parent:
            assert len(query) == 1
            return self.subtrees[0].find_nodes_with_constraints(self.conversion_dictionary[query[0]])
