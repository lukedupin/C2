from enum import Enum, auto
import uuid


class Bookmark:
    def __init__(self, name, guid=None, start=-1, end=-1 ):
        self.name = name
        self.guid = guid if guid is not None else uuid.uuid4()
        self.start_idx = start
        self.end_idx = end


class BookmarkName(Enum):
    # Generic bookmarks
    KLASS_NAME = auto()
    FUNCTION_NAME = auto()
    FUNCTION_RETURN = auto()
    FUNCTION_PARMAS = auto()
    IF_PARAMS = auto()
    FOR_PARAMS = auto()


class Token(Enum):
    ANY         = auto()
    AUTO        = auto()
    KLASS       = auto()
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
    VOID        = auto()
    CHAR        = auto()
    VAR         = auto()
    DOUBLE_COLON = auto()
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

        self.bookmarks.append( bookmark )
        return self


def createBookmark( tokens ):
    #Create the start and stops for the bookmarks
    guids = {}
    for i, token in range(len(tokens)):
        finished = list(guids.keys())
        for b in token.bookmarks:
            if b.guid not in guids:
                guids[b.guid] = [b.bookmark, i, -1]
            elif b.guid in finished:
                finished.remove( b.guid )
        for f in finished:
            guids[f][2] = i - 1

    # Build bookmarks
    bookmarks = {}
    for key in guids.keys():
        tup = guids[key]
        if tup[0] not in bookmarks:
            bookmarks[tup[0]] = Bookmark( tup[0], key, tup[1], tup[2] )

    return bookmarks


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

        ("break",                       Token.BREAK),

        ("template",                    Token.TEMPLATE),

        ("typename",                    Token.TYPENAME),

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
