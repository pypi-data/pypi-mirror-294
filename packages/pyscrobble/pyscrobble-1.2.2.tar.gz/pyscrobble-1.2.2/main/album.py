class Album:
    def __init__(self, title, artist, url, mbid, playcount, listeners, toptags, wiki, tracks, image):
        self.title = title
        self.artist = artist
        self.url = url
        self.mbid = mbid
        self.playcount = playcount
        self.listeners = listeners
        self.toptags = toptags
        self.wiki = wiki
        self.tracks = tracks
        self.image = image

    def __repr__(self):
        return f"Album(title={self.title}, artist={self.artist})"