#!/usr/bin/python

import sys

from scanner import build_rules, scanner
from patterns import group_patterns, build_paterns, build_subpatterns, match_pattern, Pattern

def main( argv ):
    rules = build_rules()
    patterns = build_paterns()
    sub_patterns = build_subpatterns()

    # Create a lookup for the pattern
    #pattern_indexs = patterns.keys()
    #sorted( pattern_indexs )

    items = []
    depth = 0

    argv.pop(0)
    for filename in argv:
        line_count = 0
        for line in open( filename ).readlines():
            line_count += 1
            for token in scanner( rules, line, line_count ):
                items.append( token )

                # Track the depth
                if token.Rule == '{':
                    depth += 1
                elif token.Rule == '}':
                    depth -= 1

                # Check if we can match a patter
                if token.Rule == ';' or token.Rule == '{':
                    pattern, offset = match_pattern( items, patterns, sub_patterns )
                    if pattern is not None:
                        if pattern == Pattern.AUTO_CLASS:
                            print("Auto class %s" % items[-1].Match )
                        elif pattern == Pattern.TEMPLATE_CLASS:
                            print("Template class %s" % items[-2].Match )

                # end of the statement
                if token.Rule == ';' or token.Rule == '{' or token.Rule == '}':
                    items.clear()


main( sys.argv )