from enum import Enum, auto


class RegexMethod(Enum):
    GREEDY  = auto()
    LAZY    = auto()


class RegexType(Enum):
    GREATER_OR_EQUAL    = auto()
    LESSER_OR_EQUAL     = auto()
    EQUAL               = auto()


class RegexSymbol:
    def __init__( self, type, method, count, token=None ):
        self.type = type
        self.method = method
        self.count = count
        self.token = token
