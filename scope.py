from enum import Enum, auto
from scanner import Token
from symbol_table import Production, Node, Symbol, SubSymbol
from regex_symbol import RegexMethod, RegexSymbol, RegexType


class Scope(Enum):
    CLASS               = auto()
    FUNCTION            = auto()
    IF                  = auto()
    WHILE               = auto()
    FOR                 = auto()
    BLOCK               = auto()


def build_scopes():
    return [Production( x[0], x[1], x[2] ) for x in (
        (Scope.CLASS,
            (Token.CLASS, Token.IDENT, RegexSymbol( RegexType.ZERO_OR_MORE, RegexMethod.GREEDY ), '{'),
            lambda production, tokens: Node(production, children=( tokens[1], ) ) ),
        (Scope.FUNCTION,
            (SubSymbol.TYPE, Token.IDENT, '(', RegexSymbol( RegexType.ZERO_OR_MORE, RegexMethod.GREEDY ), ')', '{' ),
            lambda production, tokens: Node(production, children=( tokens[0], tokens[1] ) ) ),
        (Scope.BLOCK,
            ( '{' ),
            lambda production, tokens: Node(production) ),
    )]
