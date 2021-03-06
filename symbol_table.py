from enum import Enum, auto
from scanner import Token
from regex_symbol import RegexSymbol, RegexType, RegexMethod

class Production:
    def __init__(self, production, symbols, build ):
        self.production = production
        self.symbols = symbols
        self.build = build


class Symbol(Enum):
    AUTO_KLASS          = auto()
    TEMPLATE_KLASS      = auto()
    REFLECTION          = auto()


class SubSymbol(Enum):
    TEMPLATE_LIST       = auto()
    DECLARATION         = auto()
    DECLARATION_ASSIGN  = auto()
    PARAM_LIST          = auto()
    TYPE                = auto()
    KLASS               = auto()


class Node:
    def __init__( self, production, children, start_idx, end_idx ):
        self.production = production
        self.children = []
        self.start_idx = start_idx
        self.end_idx = end_idx

        # Add the children
        if isinstance( children, list ) or isinstance( children, tuple ):
            for c in children:
                self.children.append( c )# if c is Node else Node(c) )

        else:
            self.children.append( children )

    def prepend_child(self, child):
        self.children.insert( 0, child )
        return self

    def append_child(self, child):
        self.children.append( child )
        return self


def build_subproductions():
    productions = (
        (SubSymbol.TEMPLATE_LIST,
            (Token.IDENT, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens, start, end: tokens[2].prepend_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION_ASSIGN, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens, start, end: tokens[2].prepend_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION, ',', SubSymbol.TEMPLATE_LIST),
            lambda production, tokens, start, end: tokens[2].prepend_child( tokens[0] ) ),
        (SubSymbol.TEMPLATE_LIST,
            (Token.IDENT),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION_ASSIGN),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
        (SubSymbol.TEMPLATE_LIST,
            (SubSymbol.DECLARATION),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),

#        (SubSymbol.PARAM_LIST,
#            (SubSymbol.DECLARATION_ASSIGN, ',', SubSymbol.PARAM_LIST),
#            lambda production, tokens: tokens[2].prepend_child( tokens[0] ) ),
#        (SubSymbol.PARAM_LIST,
#            (SubSymbol.DECLARATION, ',', SubSymbol.PARAM_LIST),
#            lambda production, tokens: tokens[2].prepend_child( tokens[0] ) ),
#        (SubSymbol.PARAM_LIST,
#            (SubSymbol.DECLARATION_ASSIGN),
#            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),
#        (SubSymbol.PARAM_LIST,
#            (SubSymbol.DECLARATION),
#            lambda production, tokens: Node(production, children=( tokens[0], ) ) ),

        (SubSymbol.DECLARATION,
            (SubSymbol.TYPE, Token.IDENT),
            lambda production, tokens, start, end: Node(production, ( tokens[0].children[0], tokens[1]), start, end ) ),

        (SubSymbol.DECLARATION_ASSIGN,
            (SubSymbol.TYPE, Token.IDENT, '=', Token.NUMBER),
            lambda production, tokens, start, end: Node(production, ( tokens[0].children[0], tokens[1], tokens[2], tokens[3]), start, end ) ),

        (SubSymbol.TYPE,
            (Token.DOUBLE),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
        (SubSymbol.TYPE,
            (Token.FLOAT),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
        (SubSymbol.TYPE,
            (Token.INT),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
        (SubSymbol.TYPE,
            (Token.VOID),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
        (SubSymbol.TYPE,
            (Token.CHAR),
            lambda production, tokens, start, end: Node(production, tokens[0], start, end ) ),
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
        (Symbol.REFLECTION,
             (Token.REFLECTION, Token.KLASS ),
             lambda production, tokens, start, end: Node(production, [], start, end ) ),
        (Symbol.AUTO_KLASS,
             (Token.AUTO, Token.KLASS, Token.IDENT),
             lambda production, tokens, start, end: Node(production, tokens[2], start, end ) ),
        (Symbol.TEMPLATE_KLASS,
            (Token.KLASS, Token.IDENT, '<', SubSymbol.TEMPLATE_LIST, '>' ),
            lambda production, tokens, start, end: Node(production, ( tokens[1], tokens[3] ), start, end ) ),
    )]
