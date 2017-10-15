from parser import Symbol, SubSymbol, Node
from scanner import Token, ScannerToken

def handleTemplateClass( node ):
    return (ScannerToken( Token.TEMPLATE, "template", node.children[0].Line),
            node.children[0], node.children[2])
