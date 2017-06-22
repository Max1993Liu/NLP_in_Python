from __future__ import division
from nltk.probability import ImmutableProbabilisticMixIn

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



class Production(object):

    def __init__(self, lhs, rhs):
        if not isinstance(rhs, list):
            raise TypeError("rhs needs to be a list")
        self._lhs = lhs
        self._rhs = tuple(rhs)
        self._hash = hash((self._lhs, self._rhs))


    def lhs(self):
        return self._lfs


    def rhs(self):
        return self._rhs


    def __len__(self):
        return len(self._rhs)


    def is_nonlexical(self):
        #return true if the right-hand side only contains Nonterminals
        return all(is_nonterminal(x) for x in self._rhs)


    def is_lexical(self):
        return not self.is_nonlexical()


    def __eq__(self, other):
        return (type(self) == type(other) and
                self._lhs == other._lhs and
                self._rhs == other._rhs)


    def __hash__(self):
        return self._hash



class ProbabilisticProduction(Production, ImmutableProbabilisticMixIn):

    def __init__(self, lhs, rhs, **prob):
        ImmutableProbabilisticMixIn.__init__(self, **prob)
        Production.__init__(self, lhs, rhs)


    def __str__(self):
        return Production.__unicode__(self) + \
               (' [1.0]' if (self.prob() == 1.0) else ' [%g]' % self.prob())


    def __eq__(self, other):
        return (type(self) == type(other) and
                self._lhs == other._lhs and
                self._rhs == other._rhs and
                self.prob() == other.prob())


    def __ne__(self, other):
        return not self == other


    def __hash__(self):
        return has((self._lhs, self._rhs, self.prob()))



class CFG(object):

    def __init__(self, start, productions):
        if not is_nonterminal(start):
            raise TypeError("start must be an Nonterminal")
        self._start = start
        self._productions = productions
        self._categories = set(prod.lhs() for prod in productions)
        self._calculate_indexes()
        self._calculate_grammar_forms()


    def _calculate_indexed(self):
        self._lhs_index = {}
        self._rhs_index = {}
        self._empty_index = {}
        self._lexical_index = {}
        for prod in self._productions:
            lhs = prod._lhs
            if lhs not in self._lhs_index:
                self._lhs_index[lhs] = []
            self._lhs_index[lhs].append(prod)
            if prod._rhs:
                rhs0 = prod._rhs[0]
                if rhs0 not in self._rhs_index:
                    self._rhs_index[rhs0] = []
                self._rhs_index[rhs0].append(prod)
            else:
                self._empty_index[prod.lhs()] = prod

            for token in prod._rhs:
                if is_terminal(token):
                    self._lexical_index.setdefault(token, set()).add(prod)


    def productions(self, lhs=None, rhs=None, empty=False):
        if rhs and empty:
            raise ValueError("You cannot select empty and non-empty "
                             "productions at the same time.")

            # no constraints so return everything
        if not lhs and not rhs:
            if empty:
                return self._empty_productions
            else:
                return self._productions

                # only lhs specified so look up its index
        elif lhs and not rhs:
            if empty:
                return self._empty_index.get(self._get_type_if_possible(lhs), [])
            else:
                return self._lhs_index.get(self._get_type_if_possible(lhs), [])

                # only rhs specified so look up its index
        elif rhs and not lhs:
            return self._rhs_index.get(self._get_type_if_possible(rhs), [])

            # intersect
        else:
            return [prod for prod in self._lhs_index.get(self._get_type_if_possible(lhs), [])
                    if prod in self._rhs_index.get(self._get_type_if_possible(rhs), [])]




class PCFG(CFG):

    EPSILON = 0.01

    def __init__(self, start, productions):
        #here the productions is probablistic productions
        CFG.__init__(self, start, productions)

        probs = {}
        for production in productions:
            probs[production.lhs()] = (probs.get(production.lhs(), 0) +
                                       production.prob())
        for (lhs, p) in probs.items():
            if not ((1 - PCFG.EPSILON) < p <
                        (1 + PCFG.EPSILON)):
                raise ValueError("Productions for %r do not sum to 1" % lhs)

    @classmethod
    def fromstring(cls, input, encoding=None):
        """
        Return a probabilistic ``PCFG`` corresponding to the
        input string(s).
        :param input: a grammar, either in the form of a string or else
             as a list of strings.
        """
        start, productions = read_grammar(input, standard_nonterm_parser,
                                          probabilistic=True, encoding=encoding)
        return PCFG(start, productions)



def induce_pcfg(start, productions):
    pcount = {}
    lcount = {}

    for prod in productions:
        lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1
        pcount[prod]       = pcount.get(prod,       0) + 1

    prods = [ProbabilisticProduction(p.lhs(), p.rhs(),
                                     prob=pcount[p] / lcount[p.lhs()])
             for p in pcount]
    return PCFG(start, prods)