from enum import Enum, auto
from bookmarks import  BookmarkName, Bookmark
import uuid


class Token(Enum):
    ANY         = auto()
    AUTO        = auto()
    KLASS       = auto()
    IF          = auto()
    ELSE        = auto()
    RETURN      = auto()
    WHILE       = auto()
    FOR         = auto()
    FOREACH     = auto()
    BREAK       = auto()
    TEMPLATE    = auto()
    TYPENAME    = auto()
    PUBLIC      = auto()
    PROTECTED   = auto()
    PRIVATE     = auto()
    IDENT       = auto()
    NUMBER      = auto()
    FLOAT       = auto()
    DOUBLE      = auto()
    INT         = auto()
    VOID        = auto()
    CHAR        = auto()
    VAR         = auto()
    DOUBLE_COLON= auto()
    DOT         = auto()
    VAR_EX      = auto()
    STRING      = auto()
    EQ          = auto()
    NOT         = auto()
    ASSIGN      = auto()
    ASSIGN_CONST= auto()
    REFLECTION  = auto()


class Scanner:
    def __init__(self, pattern, token):
        self.pattern = pattern
        self.token = token


class ScannerToken:
    def __init__(self, token, value, line, bookmarks=None):
        self.token = token
        self.value = value
        self.line = line
        self.bookmarks = []

        if isinstance(bookmarks, list) or isinstance(bookmarks, tuple):
            for b in bookmarks:
                self.bookmarks.append(b)
        elif bookmarks is not None:
            self.bookmarks.append(bookmarks)

    def appendBookmark(self, bookmark, guid=None ):
        if isinstance( bookmark, BookmarkName ):
            if guid is None:
                guid = uuid.uuid4()
            bookmark = Bookmark( bookmark, guid )
        assert isinstance( bookmark, Bookmark )

        #block doubles
        if any( x.bookmark == bookmark.bookmark for x in self.bookmarks ):
            return self

        self.bookmarks.append( bookmark )
        return self


def build_patterns():
    return [Scanner( x[0], x[1] ) for x in (

        ('//.*\n',                      None),
        
        ('"(?:[^\\"]|\\.)*"',           Token.STRING),

        ('[\(\)\[\]\},;]',              Token.ANY),

        ('[\{]',                        '{'),

        ("auto",                        Token.AUTO),

        ("class",                       Token.KLASS),

        ("if",                          Token.IF),

        ("else",                        Token.ELSE),

        ("var",                         Token.VAR),

        ("int",                         Token.INT),

        ("float",                       Token.FLOAT),

        ("double",                      Token.DOUBLE),

        ("void",                        Token.VOID),

        ("char",                        Token.CHAR),

        ("return",                      Token.RETURN),

        ("while",                       Token.WHILE),

        ("for",                         Token.FOR),

        ("foreach",                     Token.FOREACH),

        ("break",                       Token.BREAK),

        ("template",                    Token.TEMPLATE),

        ("typename",                    Token.TYPENAME),

        ("public",                      Token.PUBLIC),
        ("private",                     Token.PRIVATE),
        ("protected",                   Token.PROTECTED),

        ("reflection",                  Token.REFLECTION),

        ("::",                          Token.DOUBLE_COLON),

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
