#!/usr/bin/python

import sys

from scanner import scanner
from parser import parser
from lex_rules import build_patterns
from symbol_table import build_productions, build_subproductions, Symbol

from handler_auto_class import handleAutoClass
from handler_template_class import handleTemplateClass

def main( argv ):
    patterns = build_patterns()
    productions = build_productions()
    sub_productions = build_subproductions()

    depth = 0
    tokens = []

    argv.pop(0)
    for filename in argv:
        line_count = 0
        for line in open( filename ).readlines():
            line_count += 1

            # Parse the tokens
            for token in scanner( patterns, line, line_count ):
                tokens.append( token )

                # Track the depth
                if token.token == '{':
                    depth += 1
                elif token.token == '}':
                    depth -= 1

                # Are we at the end of a statement?
                if token.token != ';' and token.token != '{' and token.token != '}':
                    continue

                # Go through the indexes, attempting to match a symbol
                for production in productions:
                    node, start_idx, end_idx = parser( tokens, production.production, production.symbols, production.build, sub_productions )
                    if node is not None:
                        if node.production == Symbol.AUTO_CLASS:
                            tokens = handleAutoClass( node, tokens[0:start_idx], tokens[end_idx:] )

                        elif node.production == Symbol.TEMPLATE_CLASS:
                            tokens = handleTemplateClass( node, tokens[0:start_idx], tokens[end_idx:] )

                tokens.clear()



main( sys.argv )