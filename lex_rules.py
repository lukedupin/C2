from enum import Enum, auto

class Token(Enum):
    ANY         = auto()
    AUTO        = auto()
    CLASS       = auto()
    IF          = auto()
    ELSE        = auto()
    RETURN      = auto()
    WHILE       = auto()
    BREAK       = auto()
    TEMPLATE    = auto()
    TYPENAME    = auto()
    IDENT       = auto()
    NUMBER      = auto()
    FLOAT       = auto()
    DOUBLE      = auto()
    INT         = auto()
    VAR         = auto()
    DOT         = auto()
    VAR_EX      = auto()
    STRING      = auto()
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
        
        ('"(?:[^\\"]|\\.)*"',           Token.STRING),

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

        ("template",                    Token.TEMPLATE),

        ("typename",                    Token.TYPENAME),

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
