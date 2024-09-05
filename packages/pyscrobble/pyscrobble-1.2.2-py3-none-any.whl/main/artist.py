class Artist:
    def __init__(self, name, url, mbid, stats, similar, tags, bio, image):
        self.name = name
        self.url = url
        self.mbid = mbid
        self.stats = stats
        self.similar = similar
        self.tags = tags
        self.bio = bio
        self.image = image

    def __repr__(self):
        return f"Artist(name={self.name}, url={self.url})"