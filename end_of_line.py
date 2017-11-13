#!/usr/bin/python

from lex_rules import Token

def is_end_of_line( tokens ):
    # Are we at the end of a statement?
    if tokens[-1].token == ';' or \
       tokens[-1].token == '{' or \
       tokens[-1].token == '}':
        return True

    #Is this a special case public/private rule?
    if len(tokens) == 2 and tokens[1].token == ':' and \
       tokens[0].token in (Token.PUBLIC, Token.PROTECTED, Token.PRIVATE):
        return True

    return False
