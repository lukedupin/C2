from enum import Enum, auto
from scanner import Token


class Pattern(Enum):
    AUTO_CLASS          = auto()
    TEMPLATE_CLASS      = auto()


class SubPattern(Enum):
    TEMPLATE_LIST       = auto()
    DECLARATION         = auto()


class Node:
    def __init__( self, token, children=[], sibling=None ):
        self.token = token
        self.children = []
        self.sibling = sibling

        for c in children:
            self.children.append( c if c is Node else Node(c) )


def build_subpatterns():
    return (
        (SubPattern.TEMPLATE_LIST,
            (SubPattern.TEMPLATE_LIST, ',', Token.IDENT), lambda node: []),
        (SubPattern.TEMPLATE_LIST,
            (SubPattern.TEMPLATE_LIST, ',', SubPattern.DECLARATION), lambda node: []),
        (SubPattern.TEMPLATE_LIST,
            (Token.IDENT), lambda node: []),
        (SubPattern.TEMPLATE_LIST,
            (SubPattern.DECLARATION), lambda node: []),

        (SubPattern.DECLARATION,
            (Token.DOUBLE, Token.IDENT, '=', Token.NUMBER), lambda *args: []),
        (SubPattern.DECLARATION,
            (Token.FLOAT, Token.IDENT, '=', Token.NUMBER), lambda *args: []),
        (SubPattern.DECLARATION,
            (Token.INT, Token.IDENT, '=', Token.NUMBER),
            lambda token, *args: Node(token, children=( args[0], args[1], args[3]) ) ),
    )


def build_paterns():
    return (
        (Pattern.AUTO_CLASS,
            (Token.AUTO, Token.CLASS, Token.IDENT)
         ),
        (Pattern.TEMPLATE_CLASS,
            (Token.CLASS, Token.IDENT, '<', SubPattern.TEMPLATE_LIST, '>' )
         ),
    )


# sort the patterns into groups based on size
def group_patterns( items ):
    pat = {}
    for p in items:
        p_len = len(p[1])
        if p_len not in pat:
            pat[p_len] = []

        pat[p_len].append( p )

    return pat


def match_pattern( tokens, patterns, indexes ):
    token_len = len(tokens)

    # Go through the indexes, attempting to match a pattern
    for count in indexes:
        if token_len < count:
            return (None, None)
        offset = token_len - count

        for pattern, items in patterns[count]:
            hit = True
            for i in range(count):
                if tokens[i + offset][0] != items[i]:
                    hit = False
                    break

            if hit:
                return (pattern, offset)

    return (None, None)
