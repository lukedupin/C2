from enum import Enum, auto


class RegexMethod(Enum):
    GREEDY  = auto()
    LAZY    = auto()


class RegexType(Enum):
    ZERO_OR_MORE        = auto()
    ONE_OR_MORE         = auto()


class RegexSymbol:
    def __init__(self, type, method):
        self.type = type
        self.method = method
