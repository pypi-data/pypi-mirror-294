class Event:
    def __init__(self, title, artist, url, mbid, start_date, end_date, venue, location, attendees, headliner, lineup, description):
        self.title = title
        self.artist = artist
        self.url = url
        self.mbid = mbid
        self.start_date = start_date
        self.end_date = end_date
        self.venue = venue
        self.location = location
        self.attendees = attendees
        self.headliner = headliner
        self.lineup = lineup
        self.description = description

    def __repr__(self):
        return f"Event(title={self.title}, artist={self.artist}, start_date={self.start_date})"