from lex_rules import Token
from regex_symbol import RegexSymbol
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


def parser( tokens, production, symbols, build, sub_productions, token_idx = None ):
    #Setup my variables
    token_len = len(tokens)
    start_idx = token_idx
    nodes = []

    # Run through the symbols
    for symbol in symbols:
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
            # Can't start or end with a regex match
            if token_idx is None or token_idx + 1 >= token_len:
                return (None, 0, 0)

            # Here we are going to look through tokens, matching many of tokens until the next symbol is match based on lazy or greedy rules

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
