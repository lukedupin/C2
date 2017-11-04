import copy

from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node
from tracks import TrackType
from handler_base import handlerContainsSymbol
from scope import ScopeProductionBase, ScopeSymbol, scopeContainsSymbol, scopeTopSymbol

class ProductionAutoClass( ScopeProductionBase ):
    def __init__(self, klass="Unknown"):
        self.klass = klass
        self.template_def = []
        self.template = []
        super(ProductionAutoClass, self).__init__( Symbol.AUTO_CLASS )


def handleAutoClass( node, tokens, start, end ):
    result = [ ScannerToken( Token.CLASS, "class", node.children[0].line),
               node.children[0] ]

    return tokens[0:start] + result + tokens[end:]


def tracksAutoClass( line_tokens, symbol_matches, scope_stack ):
    # Are we not involved?
    if not handlerContainsSymbol( Symbol.AUTO_CLASS, symbol_matches, scope_stack ):
        return line_tokens

    # Is this the beginning of the class?
    if any( x == Symbol.AUTO_CLASS for x in symbol_matches ):
        tokens = line_tokens[TrackType.SOURCE]
        klass_idx = [i for i, a in enumerate(tokens) if a.token == Token.CLASS][0]

        #Move my init into the header
        line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE]
        line_tokens[TrackType.SOURCE] = []

        #Add a production to my stack
        prod = ProductionAutoClass()
        prod.klass = tokens[klass_idx + 1]
        prod.template_def = tokens[0:klass_idx - 1]
        prod.template = [x for x in tokens[0:klass_idx - 1] if x.token == Token.IDENT or x.token == ',']
        scope_stack[-1].productions.append( prod )

    # Is this the start of a function?
    elif scopeTopSymbol( scope_stack, ScopeSymbol.FUNCTION ):
        line = line_tokens[TrackType.SOURCE][0].line
        line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE][0:-1] + [ScannerToken(';', ';', line)]

#        # Add the template
#        s_line += copy.deepcopy( track_mod.template_def )
#        # Define the function minus function name
#        s_line += copy.deepcopy( tokens[0:func] )
#        # Klass name and template info
#        s_line.append( track_mod.klass )
#        # Insert template?
#        if len(track_mod.template) > 0:
#            s_line.append( ScannerToken( '<', '<', tokens[0].line) )
#            s_line += copy.deepcopy( track_mod.template )
#            s_line.append( ScannerToken( '>', '>', tokens[0].line) )
#        #Build out the function name
#        s_line.append( ScannerToken(Token.DOUBLE_COLON, '::', tokens[0].line) )
#        s_line += copy.deepcopy( tokens[func:] )
#        #s_line.append( ScannerToken(';', ';', tokens[0].line) )

    # Outside of any functions?  This is header code then
    elif not scopeContainsSymbol( scope_stack, ScopeSymbol.FUNCTION ):
        line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE]
        line_tokens[TrackType.SOURCE] = []

    return line_tokens





