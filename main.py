#!/usr/bin/python

import sys, copy

from scanner import scanner
from parser import parser
from lex_rules import build_patterns
from bookmarks import create_bookmark
from symbol_table import build_productions, build_subproductions, Symbol, Production
from scope import build_scopes, Scope, ScopeSymbol, handleScope

from handler_auto_class import handleAutoClass, tracksAutoClass
from handler_template_class import handleTemplateClass, tracksTemplateClass
from handler_reflection import handleReflection, tracksReflection
from tracks import write_track, TrackType
from end_of_line import is_end_of_line

def main( argv ):
    patterns = build_patterns()
    productions = build_productions()
    sub_productions = build_subproductions()

    scope_rules = build_scopes()

    argv.pop(0)
    for filename in argv:
        line_count = 0
        file_tracks = { TrackType.SOURCE: [], TrackType.HEADER: [] }
        tokens = []
        symbol_matches = []
        scope_stack = []

        # Read in the file contents
        for line in open( filename ).readlines():
            line_count += 1

            # Parse the tokens
            for token in scanner( patterns, line, line_count ):
                tokens.append( copy.deepcopy( token ) )

                # Are we at the end of a statement?
                if not is_end_of_line( tokens ):
                    continue

                # Go through the indexes, attempting to match a symbol
                for production in productions:
                    node = parser( tokens, production.production, production.symbols, production.build, sub_productions )
                    if node is not None:
                        symbol_matches.append( node.production )
                        if node.production == Symbol.AUTO_KLASS:
                            tokens = handleAutoClass( node, tokens )

                        elif node.production == Symbol.TEMPLATE_KLASS:
                            tokens = handleTemplateClass( node, tokens )

                        elif node.production == Symbol.REFLECTION:
                            tokens = handleReflection( node, tokens )


                # Copy the tokens into our output tracks
                line_tokens = { TrackType.SOURCE: copy.deepcopy(tokens), TrackType.HEADER: [] }

                # Increase the depth?
                stack_increased = False
                if token.token == '{':
                    stack_increased = True

                    # Setup the default scope rule
                    node = [x for x in scope_rules if x.production == ScopeSymbol.BLOCK][0]

                    # Attempt to find a better scope rule
                    for s in scope_rules:
                        tmp = parser( tokens, s.production, s.symbols, s.build, sub_productions )
                        if tmp is not None:
                            node = tmp
                            break

                    # Attach the generic bookmarks
                    tokens = handleScope( node, tokens )
                    ss = Scope( node.production, node, list() )
                    scope_stack.append( ss )


                ### Run through through all our track processors, allow them to update the output
                line_numbers = {key: len(line_tokens[key]) for key in line_tokens.keys()}
                bookmarks = create_bookmark(tokens)
                line_tokens = tracksReflection( line_tokens, bookmarks, symbol_matches, scope_stack, stack_increased, line_numbers )
                line_tokens = tracksTemplateClass( line_tokens, bookmarks, symbol_matches, scope_stack, stack_increased, line_numbers )
                line_tokens = tracksAutoClass( line_tokens, bookmarks, symbol_matches, scope_stack, stack_increased, line_numbers )


                # We've got our tracks for this line, add them to the file
                for trk in line_tokens.keys():
                    if len(line_tokens[trk]) > 0:
                        file_tracks[trk].append( line_tokens[trk] )

                #Reset my tokens so we can load another line
                if token.token == '}':
                    scope_stack.pop()
                symbol_matches.clear()
                tokens.clear()

        # Dump all the now collected tokens into the output file
        for trk in file_tracks.keys():
            write_track( filename, trk, file_tracks[trk] )



main( sys.argv )