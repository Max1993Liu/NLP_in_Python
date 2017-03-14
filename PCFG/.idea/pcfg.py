from __future__ import division

class Nonterminal(object):

    def __init__(self, symbol):
        self._symbol = symbol
        self._hash = hash(symbol)

    def symbol(self):
        return self._symbol


    def __eq__(self, other):
        return type(self) == type(other) and self._symbol == other._symbol


    def __ne__(self, other):
        return not self == other


    def __hash__(self):
        return self._hash


    def __str__(self):
        return self._symbol


    def __div__(self, rhs):
        return Nonterminal("{}/{}".format(self._symbol, rhs._symbol))


#given a string of symbol list, create non-terminals
def nonterminals(symbols):
    if "," in symbols:
        symbol_list = symbols.split(",")
    else:
        symbol_list = symbols.split()
    return [Nonterminal(s.strip()) for s in symbol_list]


def is_nonterminal(item):
    return isinstance(item, Nonterminal)


def is_terminal(item):
    return hasattr(item, '__hash__') and not isinstance(item, Nonterminal)


#https://github.com/nltk/nltk/blob/develop/nltk/grammar.py line236 production