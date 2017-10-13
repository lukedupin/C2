from enum import Enum, auto
from scanner import Token

class AutoProduction(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return start + count + 1000

class AutoSubProduction(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return start + count + 2000


class Production:
    def __init__(self, production, symbols, build ):
        self.production = production
        self.symbols = symbols
        self.build = build


class Symbol(AutoProduction):
    AUTO_CLASS          = auto()
    TEMPLATE_CLASS      = auto()


class SubSymbol(AutoSubProduction):
    TEMPLATE_LIST       = auto()
    DECLARATION         = auto()


class Node:
    def __init__( self, production, children=[], sibling=None ):
        self.production = production
        self.children = []
        self.sibling = sibling

        for c in children:
            self.children.append( c )# if c is Node else Node(c) )

    def add_child(self, child):
        self.children.append( child )
        return self


def is_token( item ):
    return int(item) < 1000


def build_subproductions():
    productions = (
        (SubSymbol.TEMPLATE_LIST,
            (Token.IDENT, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens: tokens[2].add_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens: tokens[2].add_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (Token.IDENT,),
            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION,),
            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),

        (SubSymbol.DECLARATION,
            (Token.DOUBLE, Token.IDENT, '=', Token.NUMBER),
            lambda production, tokens: Node(production, children=( tokens[0], tokens[1], tokens[3]) ) ),
        (SubSymbol.DECLARATION,
            (Token.FLOAT, Token.IDENT, '=', Token.NUMBER),
            lambda production, tokens: Node(production, children=( tokens[0], tokens[1], tokens[3]) ) ),
        (SubSymbol.DECLARATION,
            (Token.INT, Token.IDENT, '=', Token.NUMBER),
            lambda production, tokens: Node(production, children=( tokens[0], tokens[1], tokens[3]) ) ),
    )

    # Combine the productions down to a hash
    result = {}
    for x in productions:
        p = Production( x[0], x[1], x[2] )
        if p.production not in result:
            result[p.production] = []
        result[p.production].append( p )

    return result


def build_productions():
    return [Production( x[0], x[1], x[2] ) for x in (
        (Symbol.AUTO_CLASS,
            (Token.AUTO, Token.CLASS, Token.IDENT),
            lambda production, tokens: Node(production, children=( tokens[2], ) ) ),
        (Symbol.TEMPLATE_CLASS,
            (Token.CLASS, Token.IDENT, '<', SubSymbol.TEMPLATE_LIST, '>' ),
            lambda production, tokens: Node(production, children=( tokens[1], tokens[3] ) ) ),
    )]


def recursive_parser( tokens, production, symbols, build, sub_productions, token_idx = None ):
    # Deals with token start
    def token_start( token_idx, symbol, tokens, token_len ):
        # Is this my first token?  Find the starting place
        if token_idx is not None:
            return token_idx

        for t_idx in range(token_len):
            if tokens[t_idx].token == symbol:
                return t_idx

        return None

    #Setup my variables
    token_len = len(tokens)
    nodes = []

    # Run through the symbols
    for symbol in symbols:
        # Should we recurse the symbol?
        if not isinstance( symbol, SubSymbol ):
            # Handle the start of the index
            token_idx = token_start( token_idx, symbol, tokens, token_len )
            if token_idx is None or token_idx >= token_len:
                return (None, 0)

            # Go through the tokens, matching them
            if symbol == tokens[token_idx].token:
                nodes.append( tokens[token_idx] )
            else:
                return (None, 0)
            token_idx += 1

        elif symbol in sub_productions:
            node = None
            for sub in sub_productions[symbol]:
                node, token_tmp = recursive_parser( tokens, sub.production, sub.symbols, sub.build, sub_productions, token_idx )
                if node is not None:
                    token_idx = token_tmp
                    break

            # Did the recursion find a hit?  If not we failed
            if node is not None:
                nodes.append( node )
            else:
                return (None, 0)

        else:
            return (None, 0)

    return build( production, nodes ), token_idx


def parser( tokens, productions, sub_productions ):
    # Go through the indexes, attempting to match a symbol
    for production in productions:
        node, unused = recursive_parser( tokens, production.production, production.symbols, production.build, sub_productions )
        if node is not None:
            return node

    return None
