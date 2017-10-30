from lex_rules import Token, ScannerToken
from regex_symbol import RegexSymbol, RegexMethod, RegexType
from symbol_table import SubSymbol

# Deals with token start
def token_start( token_idx, symbol, tokens, token_len ):
    # Is this my first token?  Find the starting place
    if token_idx is not None:
        return token_idx

    for t_idx in range(token_len):
        if tokens[t_idx].token == symbol:
            return t_idx

    return None


def regex_match( symbol_regex, symbol_idx, token_idx, symbols, tokens ):
    # Can't start or end with a regex match
    if symbol_idx + 1 >= len(symbols) or token_idx is None or token_idx + 1 >= len(tokens):
        return None

    # Step my tokens forward
    token_idx += 1
    symbol_idx += 1

    valid_idx = None
    symbol_token = symbols[symbol_idx]
    token_len = len(tokens)
    while token_idx < token_len:
        if symbol_token.token == tokens[token_idx].token:
            valid_idx = token_idx
            if symbol_regex.method == RegexMethod.LAZY:
                return valid_idx

        token_idx += 1

    return valid_idx


def parser( tokens, production, symbols, build, sub_productions, token_idx = None ):
    #Setup my variables
    token_len = len(tokens)
    start_idx = token_idx
    nodes = []

    # Run through the symbols
    for symbol_idx, symbol in enumerate( symbols ):
        # Should we recurse the symbol?
        if isinstance( symbol, Token ):
            # Handle the start of the index
            token_idx = token_start( token_idx, symbol, tokens, token_len )
            if start_idx is None:
                start_idx = token_idx
            if token_idx is None or token_idx >= token_len:
                return (None, 0, 0)

            # Go through the tokens, matching them
            if symbol == tokens[token_idx].token:
                nodes.append( tokens[token_idx] )
            else:
                return (None, 0, 0)
            token_idx += 1

        elif isinstance( symbol, RegexSymbol ):
            # Here we are going to look through tokens, matching many of tokens until the next symbol is match based on lazy or greedy rules
            token_idx = regex_match( symbol, symbol_idx, token_idx, symbols, tokens )
            if token_idx is None:
                return (None, 0, 0)

        elif symbol in sub_productions:
            node = None
            for sub in sub_productions[symbol]:
                node, start_tmp, token_tmp = parser( tokens, sub.production, sub.symbols, sub.build, sub_productions, token_idx )
                if node is not None:
                    token_idx = token_tmp
                    break

            # Did the recursion find a hit?  If not we failed
            if node is not None:
                nodes.append( node )
            else:
                return (None, 0, 0)

        else:
            return (None, 0, 0)

    return build( production, nodes ), start_idx, token_idx
