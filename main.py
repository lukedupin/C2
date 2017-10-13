#!/usr/bin/python

import sys

from scanner import build_patterns, scanner
from parser import build_productions, build_subproductions, parser, Symbol

def main( argv ):
    patterns = build_patterns()
    productions = build_productions()
    sub_productions = build_subproductions()

    tokens = []
    depth = 0

    argv.pop(0)
    for filename in argv:
        line_count = 0
        for line in open( filename ).readlines():
            line_count += 1
            for token in scanner( patterns, line, line_count ):
                tokens.append( token )

                # Track the depth
                if token.token == '{':
                    depth += 1
                elif token.token == '}':
                    depth -= 1

                # Check if we can match a patter
                if token.token == ';' or token.token == '{':
                    node = parser( tokens, productions, sub_productions )
                    if node is not None:
                        if node.production == Symbol.AUTO_CLASS:
                            print("[AUTO] class %s" % node.children[0].value )
                        elif node.production == Symbol.TEMPLATE_CLASS:
                            print("Template class %s with template %s" % (node.children[0].value, str(node.children[1].children)) )

                # end of the statement
                if token.token == ';' or token.token == '{' or token.token == '}':
                    tokens.clear()


main( sys.argv )