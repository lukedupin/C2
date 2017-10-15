from parser import Symbol, SubSymbol
from scanner import Token

def handleAutoClass( node ):
    return (node.children[1], node.children[2])