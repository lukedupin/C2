from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node

def handleAutoClass( node, start, end ):
    tokens = [ ScannerToken( Token.CLASS, "class", node.children[0].line),
               node.children[0] ]

    return start + tokens + end
