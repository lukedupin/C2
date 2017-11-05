import copy

from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node
from tracks import TrackType
from handler_base import handlerContainsSymbol
from scope import ScopeAttributeBase, ScopeSymbol, scopeContainsSymbol, scopeTopSymbol

class AttributeAutoClass( ScopeAttributeBase ):
    def __init__(self, klass="Unknown"):
        self.klass = klass
        self.template_def = []
        self.template = []
        super(AttributeAutoClass, self).__init__( Symbol.AUTO_CLASS )


def handleAutoClass( node, tokens, start, end ):
    result = [ ScannerToken( Token.CLASS, "class", node.children[0].line),
               node.children[0] ]

    return tokens[0:start] + result + tokens[end:]


def tracksAutoClass( line_tokens, symbol_matches, scope_stack, stack_increased ):
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
        attr = AttributeAutoClass()
        attr.klass = tokens[klass_idx + 1]
        attr.template_def = tokens[0:klass_idx - 1]
        attr.template = [x for x in tokens[0:klass_idx - 1] if x.token == Token.IDENT or x.token == ',']
        scope_stack[-1].attributes.append( attr )

    # Is this the start of a function?
    elif scopeContainsSymbol( scope_stack, ScopeSymbol.FUNCTION ):
        line = line_tokens[TrackType.SOURCE][0].line
        if stack_increased:
            klass_stack = [x for x in scope_stack if x.symbol == ScopeSymbol.CLASS][0]
            func_stack = [x for x in scope_stack if x.symbol == ScopeSymbol.FUNCTION][0]
            attr = [x for x in klass_stack.attributes if x.production == Symbol.AUTO_CLASS][0]
            func_idx = func_stack.node.children[1].index

            #Add to teh header
            line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE][0:-1] + [ScannerToken(';', ';', line)]

            # Add the template
            tokens = line_tokens[TrackType.SOURCE]
            line_tokens[TrackType.SOURCE] = []
            line_tokens[TrackType.SOURCE] += copy.deepcopy( attr.template_def )
            # Define the function minus function name
            line_tokens[TrackType.SOURCE] += copy.deepcopy( tokens[0:func_idx] )
            # Klass name and template info
            line_tokens[TrackType.SOURCE].append( attr.klass )
            # Insert template?
            if len(attr.template) > 0:
                line_tokens[TrackType.SOURCE].append( ScannerToken( '<', '<', line) )
                line_tokens[TrackType.SOURCE] += copy.deepcopy( attr.template )
                line_tokens[TrackType.SOURCE].append( ScannerToken( '>', '>', line) )
            #Build out the function name
            line_tokens[TrackType.SOURCE].append( ScannerToken(Token.DOUBLE_COLON, '::', tokens[0].line) )
            line_tokens[TrackType.SOURCE] += copy.deepcopy( tokens[func_idx:] )

        #else: line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE][0:-1] + [ScannerToken(';', ';', line)]

    # Outside of any functions?  This is header code then
    else:
        line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE]
        line_tokens[TrackType.SOURCE] = []

    return line_tokens





