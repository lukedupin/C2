from lex_rules import Token, ScannerToken
from symbol_table import Symbol, SubSymbol, Node
from tracks import Track, TrackType

class ModAutoClass:
    def __init__(self, depth):
        self.depth = depth


def handleAutoClass( node, start, end ):
    tokens = [ ScannerToken( Token.CLASS, "class", node.children[0].line),
               node.children[0] ]

    return start + tokens + end

def tracksAutoClass( tokens, matches, depth, tracks ):
    # Check if we are starting an auto class
    if Symbol.AUTO_CLASS in matches:
        tracks = Track.insert_track( tracks,
                                     TrackType.SOURCE,
                                     modifiers={ Symbol.AUTO_CLASS, ModAutoClass(depth)} )
        tracks = Track.insert_track( tracks,
                                     TrackType.HEADER,
                                     modifiers={ Symbol.AUTO_CLASS, ModAutoClass(depth)} )

    # Get my source and header index, if we have any
    source = Track.find_track( tracks, TrackType.SOURCE, Symbol.AUTO_CLASS )
    header = Track.find_track( tracks, TrackType.HEADER, Symbol.AUTO_CLASS )

    # Is there no mode at all? quit
    if source is None or header is None:
        return tracks

    tracks[source].lines.append( tokens )
    tracks[header].lines.append( tokens )

    return tracks





