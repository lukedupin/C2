import re
from enum import Enum, auto


class AutoToken(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return start + count + 255


class Token(AutoToken):
    ANY         = auto()
    AUTO        = auto()
    CLASS       = auto()
    IF          = auto()
    ELSE        = auto()
    RETURN      = auto()
    WHILE       = auto()
    BREAK       = auto()
    IDENT       = auto()
    NUMBER      = auto()
    FLOAT       = auto()
    DOUBLE      = auto()
    INT         = auto()
    VAR         = auto()
    DOT         = auto()
    VAR_EX      = auto()
    EQ          = auto()
    NOT         = auto()
    ASSIGN      = auto()
    ASSIGN_CONST = auto()


class Scanner:
    def __init__(self, pattern, token):
        self.pattern = pattern
        self.token = token


class ScannerToken:
    def __init__(self, token, value, line):
        self.token = token
        self.value = value
        self.line = line


def build_patterns():
    return [Scanner( x[0], x[1] ) for x in (

        ('//.*\n',                      None),

        ('[\(\)\[\]\},;]',              Token.ANY),

        ('[\{]',                        '{'),

        ("auto",                        Token.AUTO),

        ("class",                       Token.CLASS),

        ("if",                          Token.IF),

        ("else",                        Token.ELSE),

        ("var",                         Token.VAR),

        ("int",                         Token.INT),

        ("float",                       Token.FLOAT),

        ("double",                      Token.DOUBLE),


        ("return",                      Token.RETURN),

        ("while",                       Token.WHILE),

        ("break",                       Token.BREAK),

        ('[.]',                         Token.DOT),

        ('[A-Za-z_][A-Za-z0-9_]*',      Token.IDENT),

        ('-?[0-9]+[.][0-9]+',           Token.NUMBER),
        ('-?[0-9]+',                    Token.NUMBER),

        ("\r\n",                        None),
        ("\n",                          None),
        ("\r",                          None),
        ("[ ]+",                        None),
        ("\t+",                         None),

        (".",                           Token.ANY),
    )]


def scanner( patterns, line, line_number ):
    hit = True
    while len(line) > 0:
        if not hit:
            return False
        hit = False

        # go through my patterns looking for a match
        for pattern in patterns:
            # Does this match?
            match = re.match("^(%s)" % pattern.pattern, line )
            if match is None:
                continue

            # Send out the matched pattern
            if pattern.token is not None:
                if pattern.token == Token.ANY:
                    yield ScannerToken( match[0], match[0], line_number )
                else:
                    yield ScannerToken( pattern.token, match[0], line_number )

            # Trim the line
            line = line[len(match[0]):]
            hit = True
            break
