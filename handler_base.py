from symbol_table import Symbol

def handlerContainsSymbol( symbol, symbol_matches, scope_stack ):
    if any( x == symbol for x in symbol_matches ):
        return True

    for scope in scope_stack:
        if any( x.production == symbol for x in scope.attributes ):
            return True

    return False

