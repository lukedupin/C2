import re
from lex_rules import Token, Scanner, ScannerToken

def scanner( patterns, line, line_number ):
    hit = True
    while len(line) > 0:
        if not hit:
            return False
        hit = False

        # go through my patterns looking for a match
        for pattern in patterns:
            # Does this match?
            match = re.match("^(%s)" % pattern.pattern, line )
            if match is None:
                continue

            # Send out the matched pattern
            if pattern.token is not None:
                if pattern.token == Token.ANY:
                    yield ScannerToken( match[0], match[0], line_number )
                else:
                    yield ScannerToken( pattern.token, match[0], line_number )

            # Trim the line
            line = line[len(match[0]):]
            hit = True
            break
