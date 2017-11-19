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
    #If we are zero or more, than we are already successful
    valid_idx = token_idx if symbol_regex.type == RegexType.GREATER_OR_EQUAL and symbol_regex.count <= 0 else None

    # Can't start or end with a regex match
    if symbol_idx + 1 >= len(symbols) or token_idx is None or token_idx + 1 >= len(tokens):
        return valid_idx

    # Step my tokens forward
    token_idx += 1
    symbol_idx += 1

    # Pre conditions
    match_count = 0

    #Setup and beging matching
    symbol_token = symbols[symbol_idx]
    token_len = len(tokens)
    while token_idx < token_len:
        if symbol_token == tokens[token_idx].token:
            if symbol_regex.type == RegexType.EQUAL and match_count == symbol_regex.count:
                valid_idx = token_idx
            elif symbol_regex.type == RegexType.GREATER_OR_EQUAL and match_count >= symbol_regex.count:
                valid_idx = token_idx
            elif symbol_regex.type == RegexType.LESSER_OR_EQUAL and match_count <= symbol_regex.count:
                valid_idx = token_idx
            else:
                valid_idx = None

            if symbol_regex.method == RegexMethod.LAZY:
                return valid_idx

        # Are we matching the tokens we ment to?
        if symbol_regex.token is not None and symbol_regex.token != tokens[token_idx].token:
            return valid_idx

        token_idx += 1
        match_count += 1

    return valid_idx


# Main goal here is to find the best match, starting at zero index, to the end
def parser( tokens, production, symbols, build, sub_productions ):
    for idx in range( len(tokens) ):
        node = parser_recurse( tokens, production, symbols, build, sub_productions, idx )
        if node is not None:
            return node

    return None


def parser_recurse( tokens, production, symbols, build, sub_productions, token_idx ):
    #Setup my variables
    token_len = len(tokens)
    start_idx = token_idx
    nodes = []

    # Not happening?
    if token_idx >= token_len:
        return None

    # Run through the symbols
    for symbol_idx, symbol in enumerate( symbols ):
        # Should we recurse the symbol?
        if isinstance( symbol, Token ) or isinstance( symbol, str ):
            if token_idx is None or token_idx >= token_len:
                return None

            # Go through the tokens, matching them
            if symbol == tokens[token_idx].token:
                nodes.append( tokens[token_idx] )
            else:
                return None
            token_idx += 1

        elif isinstance( symbol, RegexSymbol ):
            # Here we are going to look through tokens, matching many of tokens until the next symbol is match based on lazy or greedy rules
            token_idx = regex_match( symbol, symbol_idx, token_idx, symbols, tokens )
            if token_idx is None or token_idx >= token_len:
                return None

        elif symbol in sub_productions:
            node = None
            for sub in sub_productions[symbol]:
                node = parser_recurse( tokens, sub.production, sub.symbols, sub.build, sub_productions, token_idx )
                if node is not None:
                    token_idx = node.end_idx
                    break

            # Did the recursion find a hit?  If not we failed
            if node is not None:
                nodes.append( node )
            else:
                return None

        else:
            return None

    return build( production, nodes, start_idx, token_idx )
