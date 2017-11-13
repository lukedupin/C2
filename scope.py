from enum import Enum, auto
from scanner import Token
from symbol_table import Production, Node, Symbol, SubSymbol
from regex_symbol import RegexMethod, RegexSymbol, RegexType
from lex_rules import BookmarkName


class ScopeAttributeBase:
    def __init__(self, production):
        self.production = production


class Scope:
    def __init__(self, symbol, node, attributes=[] ):
        self.symbol = symbol
        self.node = node
        self.attributes = attributes


class ScopeSymbol(Enum):
    KLASS               = auto()
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
        (ScopeSymbol.KLASS,
            (Token.KLASS, Token.IDENT, RegexSymbol( RegexType.ZERO_OR_MORE, RegexMethod.GREEDY ), '{'),
            lambda production, tokens, start, end: Node(production, tokens[1], start, end ) ),
        (ScopeSymbol.FUNCTION,
            (SubSymbol.TYPE, Token.IDENT, '(', RegexSymbol( RegexType.ZERO_OR_MORE, RegexMethod.GREEDY ), ')', '{' ),
            lambda production, tokens, start, end: Node(production, ( tokens[0], tokens[1] ), start, end ) ),
        (ScopeSymbol.BLOCK,
            ( '{' ),
            lambda production, tokens, start, end: Node(production, start_idx=start, end_idx=end ) ),
    )]


def handleScope( node, tokens ):
    if node.production == ScopeSymbol.KLASS:
        tokens[node.start_idx + 1].appendBookmark( BookmarkName.KLASS_NAME )

    elif node.production == ScopeSymbol.FUNCTION:
        tokens[node.start_idx].appendBookmark( BookmarkName.FUNCTION_RETURN )
        tokens[node.start_idx + 1].appendBookmark( BookmarkName.FUNCTION_NAME )

    return tokens
