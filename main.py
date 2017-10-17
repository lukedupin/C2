#!/usr/bin/python

import sys, copy

from scanner import scanner
from parser import parser
from lex_rules import build_patterns
from symbol_table import build_productions, build_subproductions, Symbol, Production
from scope import build_scopes, Scope

from handler_auto_class import handleAutoClass, tracksAutoClass
from handler_template_class import handleTemplateClass
from tracks import write_track, Track, TrackType

def main( argv ):
    patterns = build_patterns()
    productions = build_productions()
    sub_productions = build_subproductions()

    scope_rules = build_scopes()

    argv.pop(0)
    for filename in argv:
        line_count = 0
        tracks = []
        tokens = []
        matches = []
        scope_stack = []

        # Read in the file contents
        for line in open( filename ).readlines():
            line_count += 1

            # Parse the tokens
            for token in scanner( patterns, line, line_count ):
                tokens.append( token )

                # Are we at the end of a statement?
                if token.token != ';' and token.token != '{' and token.token != '}':
                    tokens.append( token )
                    continue

                # Go through the indexes, attempting to match a symbol
                for production in productions:
                    node, start_idx, end_idx = parser( tokens, production.production, production.symbols, production.build, sub_productions )
                    if node is not None:
                        matches.append( node.production )
                        if node.production == Symbol.AUTO_CLASS:
                            tokens = handleAutoClass( node, tokens[0:start_idx], tokens[end_idx:] )

                        elif node.production == Symbol.TEMPLATE_CLASS:
                            tokens = handleTemplateClass( node, tokens[0:start_idx], tokens[end_idx:] )

                # We've got the raw tokens, now pass that completed set of tokens into the track creates to build out tracks
                handled = False
                if not handled:
                    tracks, handled = tracksAutoClass( tokens, matches, depth, tracks )
                if not handled:
                    #tracks = tracksTemplateclass( tokens, matches, depth, tracks )
                    pass
                if not handled:
                    tracks = Track.insert_track( tracks, TrackType.SOURCE )
                    source = Track.find_track( tracks, TrackType.SOURCE )
                    tracks[source].lines.append( copy.deepcopy(tokens) )
                tokens.clear()

                # Increase the depth
                if token.token == '{':
                    scope = Production( Scope.BLOCK )
                    for s in scope_rules:
                        tmp, unused0, unused1 = parser( tokens, production.production, production.symbols, production.build, sub_productions )
                        if tmp is not None:
                            scope = tmp
                            break

                    scope.append( scope )
                if token.token == '}':
                    scope.pop()

        # Dump all the now collected tokens into the output file
        for track in tracks:
            write_track( track )



main( sys.argv )