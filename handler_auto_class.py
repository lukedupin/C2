import copy

from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node
from tracks import Track, TrackType

class ModAutoClass:
    def __init__(self, depth):
        self.depth = depth
        self.klass = "Tmp name"
        self.template_def = []
        self.template = []


def handleAutoClass( node, start, end ):
    tokens = [ ScannerToken( Token.CLASS, "class", node.children[0].line),
               node.children[0] ]

    return start + tokens + end

def tracksAutoClass( tokens, matches, depth, tracks ):
    # Check if we are starting an auto class
    if Symbol.AUTO_CLASS in matches:
        tracks = Track.insert_track( tracks,
                                     TrackType.SOURCE,
                                     modifiers={ Symbol.AUTO_CLASS: ModAutoClass(depth)} )
        tracks = Track.insert_track( tracks,
                                     TrackType.HEADER,
                                     modifiers={ Symbol.AUTO_CLASS: ModAutoClass(depth)} )

    # Get my source and header index, if we have any
    source = Track.find_track( tracks, TrackType.SOURCE, Symbol.AUTO_CLASS )
    header = Track.find_track( tracks, TrackType.HEADER, Symbol.AUTO_CLASS )

    # Is there no mode at all? quit
    if source is None or header is None:
        return tracks, False

    # Get the track info
    s_line = []
    h_line = []
    track = tracks[source]
    track_mod = track.modifiers[Symbol.AUTO_CLASS]

    # Is this the beginning of the class?
    if any( x.token == Token.CLASS for x in tokens ) and tokens[-1].token == '{':
        klass_idx = [i for i, a in enumerate(tokens) if a.token == Token.CLASS][0]
        track_mod.klass = tokens[klass_idx + 1]
        track_mod.template_def = tokens[0:klass_idx - 1]
        track_mod.template = [x for x in tokens[0:klass_idx - 1] if x.token == Token.IDENT or x.token == ',']

        #tracks[source].modifiers[Symbol.AUTO_CLASS].klass = tokens[klass_idx + 1]
        #tracks[source].modifiers[Symbol.AUTO_CLASS].template_def = tokens[0:klass_idx - 1]
        #tracks[source].modifiers[Symbol.AUTO_CLASS].template = [x for x in tokens[0:klass_idx - 1] if x.token == Token.IDENT or x.token == ',']

        h_line += copy.deepcopy( tokens )# + [ScannerToken(';', ';', tokens[0].line)]

    # Function def?
    elif any( x.token == '(' for x in tokens ) and tokens[-1].token == '{':
        func = [i for i, a in enumerate(tokens) if a.token == '('][0] - 1

        h_line = tokens[0:-1] + [ScannerToken(';', ';', tokens[0].line)]

        # Add the template
        s_line += copy.deepcopy( track_mod.template_def )
        # Define the function minus function name
        s_line += copy.deepcopy( tokens[0:func] )
        #Klass name and template info
        s_line.append( track_mod.klass )
        if len(track_mod.template) > 0:
            s_line.append( ScannerToken( '<', '<', tokens[0].line) )
            s_line += copy.deepcopy( track_mod.template )
            s_line.append( ScannerToken( '>', '>', tokens[0].line) )
        s_line.append( ScannerToken(Token.DOUBLE_COLON, '::', tokens[0].line) )
        s_line += copy.deepcopy( tokens[func:] )
        #s_line.append( ScannerToken(';', ';', tokens[0].line) )

    else:
        return tracks, False

    #Add the result
    if len(s_line) > 0:
        tracks[source].lines.append( s_line )
    if len(h_line) > 0:
        tracks[header].lines.append( h_line )

    return tracks, True





