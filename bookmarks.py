from enum import Enum, auto
import uuid


class Bookmark:
    def __init__(self, bookmark, guid=None, start=-1, end=-1 ):
        self.bookmark = bookmark
        self.guid = guid if guid is not None else uuid.uuid4()
        self.start_idx = start
        self.end_idx = end


class BookmarkName(Enum):
    # Generic bookmarks
    KLASS_NAME = auto()
    FUNCTION_NAME = auto()
    FUNCTION_RETURN = auto()
    FUNCTION_PARMAS = auto()
    IF_PARAMS = auto()
    FOR_PARAMS = auto()


def create_bookmark( tokens ):
    #Create the start and stops for the bookmarks
    guids = {}
    for i, token in enumerate(tokens):
        hits = []
        for b in token.bookmarks:
            hits.append( b.guid )
            if b.guid not in guids:
                guids[b.guid] = [b.bookmark, i, -1]

        for guid in guids.keys():
            if guid not in hits and guids[guid][2] < 0:
                guids[guid][2] = i - 1

    # Build bookmarks
    bookmarks = {}
    for key in guids.keys():
        tup = guids[key]
        if tup[0] not in bookmarks:
            bookmarks[tup[0]] = []
        if tup[2] < 0:
            tup[2] = len(tokens) - 1
        bookmarks[tup[0]].append( Bookmark( tup[0], key, tup[1], tup[2] ) )

    return bookmarks
