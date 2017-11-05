from enum import Enum, auto
from scanner import Token
from symbol_table import Production, Node, Symbol, SubSymbol
from regex_symbol import RegexMethod, RegexSymbol, RegexType


class ScopeAttributeBase:
    def __init__(self, production):
        self.production = production


class Scope:
    def __init__(self, symbol, node, attributes=[] ):
        self.symbol = symbol
        self.node = node
        self.attributes = attributes


class ScopeSymbol(Enum):
    CLASS               = auto()
    FUNCTION            = auto()
    IF                  = auto()
    WHILE               = auto()
    FOR                 = auto()
    BLOCK               = auto()


def scopeContainsSymbol( scope_stack, symbol ):
    return any( x.symbol == symbol for x in scope_stack )


def scopeTopSymbol( scope_stack, symbol ):
    return len(scope_stack) > 0 and scope_stack[-1].symbol == symbol


def build_scopes():
    return [Production( x[0], x[1], x[2] ) for x in (
        (ScopeSymbol.CLASS,
            (Token.CLASS, Token.IDENT, RegexSymbol( RegexType.ZERO_OR_MORE, RegexMethod.GREEDY ), '{'),
            lambda production, tokens: Node(production, children=( tokens[1], ) ) ),
        (ScopeSymbol.FUNCTION,
            (SubSymbol.TYPE, Token.IDENT, '(', RegexSymbol( RegexType.ZERO_OR_MORE, RegexMethod.GREEDY ), ')', '{' ),
            lambda production, tokens: Node(production, children=( tokens[0], tokens[1] ) ) ),
        (ScopeSymbol.BLOCK,
            ( '{' ),
            lambda production, tokens: Node(production) ),
    )]
