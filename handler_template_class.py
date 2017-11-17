from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node
from scope import ScopeAttributeBase


def handleTemplateClass( node, tokens ):
    result = [ ScannerToken( Token.TEMPLATE, "template", node.children[0].line),
               ScannerToken( '<', '<', node.children[0].line) ]

    # Add in my template list
    for idx, child in enumerate( node.children[1].children ):
        if idx > 0:
            result.append( ScannerToken( ',', ',', node.children[0].line) )
        if isinstance( child, ScannerToken ):
            result += ( ScannerToken( Token.TYPENAME, "typename", node.children[0].line), child)
        else:
            result += child.children

    #Add in the class
    result += ( ScannerToken( '>', '>', node.children[0].line),
                ScannerToken( Token.KLASS, "class", node.children[0].line),
                node.children[0])

    return tokens[0:node.start_idx] + result + tokens[node.end_idx:]
