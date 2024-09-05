class LastFMError(Exception):
    pass

class RateLimitExceeded(LastFMError):
    pass

class InvalidAPIKey(LastFMError):
    pass

class ArtistNotFoundError(LastFMError):
    pass

class AlbumNotFoundError(LastFMError):
    pass

class TrackNotFoundError(LastFMError):
    pass

class UserNotFoundError(LastFMError):
    pass
