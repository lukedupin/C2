from parser import Symbol, SubSymbol, Node
from scanner import Token, ScannerToken

def handleAutoClass( node, start, end ):
    tokens = [ ScannerToken( Token.CLASS, "class", node.children[0].line),
               node.children[0] ]

    return start + tokens + end
