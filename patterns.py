from enum import Enum, auto
from scanner import Token

class AutoPattern(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return start + count + 1000

class AutoSubPattern(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return start + count + 2000


class ParserPattern:
    def __init__(self, rule, patterns, build ):
        self.Rule = rule
        self.Patterns = patterns
        self.Build = build


class Pattern(AutoPattern):
    AUTO_CLASS          = auto()
    TEMPLATE_CLASS      = auto()


class SubPattern(AutoSubPattern):
    TEMPLATE_LIST       = auto()
    DECLARATION         = auto()


class Node:
    def __init__( self, token, children=[], sibling=None ):
        self.token = token
        self.children = []
        self.sibling = sibling

        for c in children:
            self.children.append( c if c is Node else Node(c) )


def is_token( item ):
    return int(item) < 1000


def build_subpatterns():
    patterns = (
        ParserPattern(SubPattern.TEMPLATE_LIST,
            (SubPattern.TEMPLATE_LIST, ',', Token.IDENT),
            lambda token, args: Node(token, sibling=args[0] ) ),
        ParserPattern(SubPattern.TEMPLATE_LIST,
            (SubPattern.TEMPLATE_LIST, ',', SubPattern.DECLARATION),
            lambda token, args: Node(token, sibling=args[0] ) ),
        ParserPattern(SubPattern.TEMPLATE_LIST,
            (Token.IDENT),
            lambda token, args: Node(token, children=( args[0], ) ) ),
        ParserPattern(SubPattern.TEMPLATE_LIST,
            (SubPattern.DECLARATION),
            lambda token, args: Node(token, children=( args[0], ) ) ),

        ParserPattern(SubPattern.DECLARATION,
            (Token.DOUBLE, Token.IDENT, '=', Token.NUMBER),
            lambda token, args: Node(token, children=( args[0], args[1], args[3]) ) ),
        ParserPattern(SubPattern.DECLARATION,
            (Token.FLOAT, Token.IDENT, '=', Token.NUMBER),
            lambda token, args: Node(token, children=( args[0], args[1], args[3]) ) ),
        ParserPattern(SubPattern.DECLARATION,
            (Token.INT, Token.IDENT, '=', Token.NUMBER),
            lambda token, args: Node(token, children=( args[0], args[1], args[3]) ) ),
    )

    # Combine the rules down to a hash
    result = {}
    for pattern in patterns:
        if pattern.Rule not in result:
            result[pattern.Rule] = []
        result[pattern.Rule].append( pattern )

    return result


def build_paterns():
    return (
        ParserPattern(Pattern.AUTO_CLASS,
            (Token.AUTO, Token.CLASS, Token.IDENT),
            lambda token, args: Node(token, children=( args[2]) ) ),
        ParserPattern(Pattern.TEMPLATE_CLASS,
            (Token.CLASS, Token.IDENT, '<', SubPattern.TEMPLATE_LIST, '>' ),
            lambda token, args: Node(token, children=( args[1], args[3] ) ) ),
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

def recursive_match( tokens, match, patterns, build, sub_patterns, token_idx = None ):
    # Deals with token start
    def token_start( token_idx, pattern, tokens, token_len ):
        # Is this my first token?  Find the starting place
        if token_idx is not None:
            return token_idx

        for t_idx in range(token_len):
            if tokens[t_idx].Rule == pattern:
                return t_idx

        return None

    #Setup my variables
    token_len = len(tokens)
    nodes = []

    # Run through the patterns
    for pattern in patterns:
        # Should we recurse the pattern?
        if not isinstance( pattern, SubPattern ):
            # Handle the start of the index
            token_idx = token_start( token_idx, pattern, tokens, token_len )
            if token_idx is None or token_idx >= token_len:
                return (None, 0)

            # Go through the tokens, matching them
            if pattern == tokens[token_idx].Rule:
                nodes.append( tokens[token_idx] )
            else:
                return (None, 0)
            token_idx += 1

        else:
            node, token_idx = recursive_match( tokens, match, patterns, build, sub_patterns, token_idx )
            if node is None:
                return (None, 0)

            nodes.append( node )

    return build( match, nodes ), token_idx + 1


def match_pattern( tokens, pattern_matches, sub_patterns ):
    # Go through the indexes, attempting to match a pattern
    for pattern in pattern_matches:
        node, unused = recursive_match( tokens, pattern.Rule, pattern.Patterns, pattern.Build, sub_patterns )
        if node is not None:
            print( node )

    return (None, None)
