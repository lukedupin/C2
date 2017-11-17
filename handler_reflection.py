import copy

from lex_rules import Token, ScannerToken, Bookmark, BookmarkName
from symbol_table import Symbol, SubSymbol, Node
from tracks import TrackType
from handler_base import handlerContainsSymbol
from scope import ScopeAttributeBase, ScopeSymbol, scopeContainsSymbol, scopeTopSymbol


class AttributeReflection( ScopeAttributeBase ):
    def __init__(self, insert_line ):
        self.insert_line = insert_line
        self.klass = "None"
        self.members = { Token.PUBLIC: [], Token.PROTECTED: [], Token.PRIVATE: [] }
        self.functions = { Token.PUBLIC: [], Token.PROTECTED: [], Token.PRIVATE: [] }
        super(AttributeReflection, self).__init__( Symbol.REFLECTION )


def handleReflection( node, tokens ):
    #All we do here is remove the "reflection" We'll store the insert line in the tracks
    return tokens[0:node.start_idx] + tokens[node.end_idx:]


def tracksReflection( line_tokens, bookmarks, symbol_matches, scope_stack, stack_increased, line_numbers ):
    # Are we not involved?
    if not handlerContainsSymbol( Symbol.REFLECTION, symbol_matches, scope_stack ):
        return line_tokens

    # Is this the beginning of the class?
    if any( x == Symbol.REFLECTION for x in symbol_matches ):
        #Add a production to my stack
        attr = AttributeReflection( line_numbers[TrackType.HEADER] )
        scope_stack[-1].attributes.append( attr )

    # Is this the start of a function?
    elif stack_increased and scope_stack[-1].symbol == ScopeSymbol.FUNCTION:
        klass_stack = [x for x in scope_stack if x.symbol == ScopeSymbol.KLASS][0]
        func_stack = [x for x in scope_stack if x.symbol == ScopeSymbol.FUNCTION][0]
        attr = [x for x in klass_stack.attributes if x.production == Symbol.REFLECTION][0]
        func_idx = bookmarks[BookmarkName.FUNCTION_NAME][0].start_idx

        # Grab my tokens
        tokens = line_tokens[TrackType.SOURCE]

        # Define the function minus function name
        attr.functions[Token.PUBLIC].append( tokens[func_idx].value )

    return line_tokens





