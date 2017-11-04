from enum import Enum, auto
import copy

class TrackType(Enum):
    SOURCE = auto()
    HEADER = auto()


def write_track( filename, track, lines ):
    print("")
    print("%s %s" % (filename, str(track)) )
    print("")
    for line in lines:
        print( " ".join([x.value for x in line]) )
