class Track:
    def __init__(self, name, artist, album, url, duration, playcount, mbid, listeners, toptags, wiki, streamable, fulltrack):
        self.name = name
        self.artist = artist
        self.album = album
        self.url = url
        self.duration = duration
        self.playcount = playcount
        self.mbid = mbid
        self.listeners = listeners
        self.toptags = toptags
        self.wiki = wiki
        self.streamable = streamable
        self.fulltrack = fulltrack

    def __repr__(self):
        return f"Track(name={self.name}, artist={self.artist}, album={self.album})"