import copy

from lex_rules import Token, ScannerToken, Bookmark, BookmarkName
from symbol_table import Symbol, SubSymbol, Node
from tracks import TrackType
from handler_base import handlerContainsSymbol
from scope import ScopeAttributeBase, ScopeSymbol, scopeContainsSymbol, scopeTopSymbol

class AttributeAutoClass( ScopeAttributeBase ):
    def __init__(self, klass="Unknown"):
        self.klass = klass
        self.template_def = []
        self.template = []
        super(AttributeAutoClass, self).__init__( Symbol.AUTO_KLASS )


def handleAutoClass( node, tokens ):
    klass = copy.deepcopy( node.children[0] ).appendBookmark( BookmarkName.KLASS_NAME )

    return tokens[0:node.start_idx] + \
           [ ScannerToken( Token.KLASS, "class", klass.line), klass ] + \
           tokens[node.end_idx:]


def tracksAutoClass( line_tokens, bookmarks, symbol_matches, scope_stack, stack_increased ):
    # Are we not involved?
    if not handlerContainsSymbol( Symbol.AUTO_KLASS, symbol_matches, scope_stack ):
        return line_tokens

    # Is this the beginning of the class?
    if any( x == Symbol.AUTO_KLASS for x in symbol_matches ):
        tokens = line_tokens[TrackType.SOURCE]
        klass_idx = bookmarks[BookmarkName.KLASS_NAME][0].start_idx

        #Move my init into the header
        line_tokens[TrackType.HEADER] = line_tokens[TrackType.SOURCE]
        line_tokens[TrackType.SOURCE] = []

        #Add a production to my stack
        attr = AttributeAutoClass()
        attr.klass = tokens[klass_idx]
        attr.template_def = tokens[0:klass_idx - 1]
        attr.template = [x for x in tokens[0:klass_idx] if x.token == Token.IDENT or x.token == ',']
        scope_stack[-1].attributes.append( attr )

    # Is this the start of a function?
    elif scopeContainsSymbol( scope_stack, ScopeSymbol.FUNCTION ):
        line = line_tokens[TrackType.SOURCE][0].line
        if stack_increased:
            klass_stack = [x for x in scope_stack if x.symbol == ScopeSymbol.KLASS][0]
            func_stack = [x for x in scope_stack if x.symbol == ScopeSymbol.FUNCTION][0]
            attr = [x for x in klass_stack.attributes if x.production == Symbol.AUTO_KLASS][0]
            func_idx = bookmarks[BookmarkName.FUNCTION_NAME][0].start_idx

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





