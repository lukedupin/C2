from enum import Enum, auto
import copy

class TrackType(Enum):
    SOURCE = auto()
    HEADER = auto()
    BOTH   = auto()


#Handles a single track, holds currenty track handler info
class Track:
    def __init__(self, type, modifiers=None, lines=[] ):
        self.type = type
        self.modifiers = {}
        self.lines = []

        if modifiers is not None:
            self.modifiers = { **modifiers }

    # Adds a new modifier if one is given, force will force add, otherwise it'll only add if not exists
    def add_modifier(self, modifier, force=True):
        if modifier is None:
            return self

        if force:
            self.modifiers = { **self.modifiers, **modifier }
        else:
            self.modifiers = { **modifier, **self.modifiers }
        return self

    # Kill a modifier and return the Track object
    def remove_modifier(self, modifier):
        if modifier is not None:
            self.modifiers.pop( modifier, None )
        return self

    @staticmethod
    def find_track( tracks, type, mod=None ):
        indexes = [i for i in range(len(tracks)) if tracks[i].type == type]
        if len(indexes) > 1 and mod is not None:
            indexes = [i for i in indexes if mod in tracks[i].modifiers]

        return indexes[0] if len(indexes) == 1 else None

    # This will insert a track into tracks if it doesn't exist
    @staticmethod
    def insert_track( tracks, type, mod=None, modifiers=None ):
        index = Track.find_track(tracks, type, mod)
        if index is None:
            tracks = copy.deepcopy(tracks)
            tracks.append( Track( type, {**modifiers} if modifiers is not None else None ) )
            index = len(tracks) - 1

        # Add in the modifier
        tracks[index].add_modifier( modifiers, force=False )
        return tracks


def write_track( track ):
    for line in track.lines:
        print( " ".join([x.value for x in line]) )
