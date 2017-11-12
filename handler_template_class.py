from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node

def handleTemplateClass( node, start, end ):
    tokens = [ ScannerToken( Token.TEMPLATE, "template", node.children[0].line),
               ScannerToken( '<', '<', node.children[0].line) ]

    # Add in my template list
    for idx, child in enumerate( node.children[1].children ):
        if idx > 0:
            tokens.append( ScannerToken( ',', ',', node.children[0].line) )
        if isinstance( child, ScannerToken ):
            tokens += ( ScannerToken( Token.TYPENAME, "typename", node.children[0].line), child)
        else:
            tokens += child.children

    #Add in the class
    tokens += ( ScannerToken( '>', '>', node.children[0].line),
                ScannerToken( Token.KLASS, "class", node.children[0].line),
                node.children[0])

    return start + tokens + end
