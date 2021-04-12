from __future__ import annotations

from typing import Union, Optional, List
from bst import BinarySearchTree


class DecisionTree:
    def __init__(self, category: Optional[str], is_binary_parent: bool):
        self.subtrees = []
        self.category = category
        self._is_binary_parent = is_binary_parent

    def add_subtree(self, subtree: Union[BinarySearchTree, DecisionTree]):
        self.subtrees.append(subtree)

    def evaluate(self, query: List):
        if not self._is_binary_parent:
            for item in self.subtrees:
                if item.category == query[0]:
                    return item.evaluate(query[1:])
        elif self._is_binary_parent:
            assert len(query) == 1

            return self.subtrees[0].find_greater_or_equal_nodes(query[0])
