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
    DECLARATION_ASSIGN  = auto()
    TYPE                = auto()


class Node:
    def __init__( self, production, children=[], sibling=None ):
        self.production = production
        self.children = []
        self.sibling = sibling

        # Add the children
        if isinstance( children, list ) or isinstance( children, tuple ):
            for c in children:
                self.children.append( c )# if c is Node else Node(c) )

        else:
            self.children = (children, )

    def prepend_child(self, child):
        self.children.insert( 0, child )
        return self

    def append_child(self, child):
        self.children.append( child )
        return self


def is_token( item ):
    return int(item) < 1000


def build_subproductions():
    productions = (
        (SubSymbol.TEMPLATE_LIST,
            (Token.IDENT, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens: tokens[2].prepend_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION_ASSIGN, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens: tokens[2].prepend_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens: tokens[2].prepend_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (Token.IDENT),
            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION_ASSIGN),
            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION),
            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),

        (SubSymbol.DECLARATION,
            (SubSymbol.TYPE, Token.IDENT),
            lambda production, tokens: Node(production, children=( tokens[0].children[0], tokens[1]) ) ),

        (SubSymbol.DECLARATION_ASSIGN,
            (SubSymbol.TYPE, Token.IDENT, '=', Token.NUMBER),
            lambda production, tokens: Node(production, children=( tokens[0].children[0], tokens[1], tokens[2], tokens[3]) ) ),

        (SubSymbol.TYPE,
            (Token.DOUBLE),
            lambda production, tokens: Node(production, children=( tokens[0]) ) ),
        (SubSymbol.TYPE,
            (Token.FLOAT),
            lambda production, tokens: Node(production, children=( tokens[0]) ) ),
        (SubSymbol.TYPE,
            (Token.INT),
            lambda production, tokens: Node(production, children=( tokens[0]) ) ),
    )

    # Combine the productions down to a hash
    result = {}
    for x in productions:
        symbols = x[1] if isinstance( x[1], tuple ) else (x[1], )
        p = Production( x[0], symbols, x[2] )
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


# Deals with token start
def token_start( token_idx, symbol, tokens, token_len ):
    # Is this my first token?  Find the starting place
    if token_idx is not None:
        return token_idx

    for t_idx in range(token_len):
        if tokens[t_idx].token == symbol:
            return t_idx

    return None


def parser( tokens, production, symbols, build, sub_productions, token_idx = None ):
    #Setup my variables
    token_len = len(tokens)
    start_idx = token_idx
    nodes = []

    # Run through the symbols
    for symbol in symbols:
        # Should we recurse the symbol?
        if not isinstance( symbol, SubSymbol ):
            # Handle the start of the index
            token_idx = token_start( token_idx, symbol, tokens, token_len )
            if start_idx is None:
                start_idx = token_idx
            if token_idx is None or token_idx >= token_len:
                return (None, 0, 0)

            # Go through the tokens, matching them
            if symbol == tokens[token_idx].token:
                nodes.append( tokens[token_idx] )
            else:
                return (None, 0, 0)
            token_idx += 1

        elif symbol in sub_productions:
            node = None
            for sub in sub_productions[symbol]:
                node, start_tmp, token_tmp = parser( tokens, sub.production, sub.symbols, sub.build, sub_productions, token_idx )
                if node is not None:
                    token_idx = token_tmp
                    break

            # Did the recursion find a hit?  If not we failed
            if node is not None:
                nodes.append( node )
            else:
                return (None, 0, 0)

        else:
            return (None, 0, 0)

    return build( production, nodes ), start_idx, token_idx
