from nltk.grammar import Production, Nonterminal
import re

class Tree(list):

    def __init__(self, node, children=None):
        if children is None:
            raise ValueError("Children needs to be a list")
        elif not isinstance(children, list):
            raise TypeError("children needs to be a list")
        else:
            super(Tree, self).__init__(children)
            self._label = node

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                (self._label, list(self)) == (other._label, list(other)))


    def __ne__(self, other):
        return not self==other


    def __getitem__(self, index):
        if isinstance(index, (int, slice)):
            return super(Tree, self).__getitem__(index)
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                return self
            elif len(index) == 1:
                return self[index[0]]
            else:
                return self[index[0]][index[1:]]
        else:
            raise TypeError("Wrong type for indexing")


    def __setitem__(self, index, value):
        if isinstance(index, (int, slice)):
            return super(Tree, self).__setitem__(index, value)
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                raise IndexError("The tree position () may not be assigned to!")
            elif len(index) == 1:
                self[index[0]] = value
            else:
                self[index[0]][index[1:]] = value
        else:
            raise TypeError("indice must be integers")


    def __delitem__(self, index):
        if isinstance(index, (int, slice)):
            return super(Tree, self).__delitem__(self, index)
        elif isinstance(index, (list, tuple)):
            if len(index) == 0:
                raise IndexError("The tree position () may not be deleted")
            elif len(index) == 1:
                del self[index[0]]
            else:
                del self[index[0]][index[1:]]
        else:
            raise TypeError("indice must be integer")


    def label(self):
        return self._label


    def set_label(self, label):
        self._label = label


    def leaves(self):
        leaves = []
        for child in self:
            if isinstance(child, Tree):
                leaves.extend(child.leaves())
            else:
                leaves.append(child)
        return leaves


    def flatten(self):
        return Tree(self.label(), self.leaves())


    def height(self):
        max_child_height = 0
        for child in self:
            if isinstance(child, Tree):
                max_child_height = max(max_child_height, child.height())
            else:
                max_child_height = max(max_child_height, 1)
        return 1 + max_child_height


    def subtrees(self, filter=None):
        if not filter or filter(self):
            yield self
        for child in self:
            if isinstance(child, Tree):
                for subtree in child.subtrees(filter):
                    yield subtree



