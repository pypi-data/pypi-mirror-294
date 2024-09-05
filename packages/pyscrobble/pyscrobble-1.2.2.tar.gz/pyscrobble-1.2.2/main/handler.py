import requests
import xmltodict
import logging
import json
from .exceptions import RateLimitExceeded, InvalidAPIKey, ArtistNotFoundError, AlbumNotFoundError, TrackNotFoundError, LastFMError
from .ratelimiter import RateLimiter
from .track import Track
from .album import Album
from .user import User
from .event import Event
from .artist import Artist
from .shout import Shout


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Handler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.rate_limiter = RateLimiter(max_requests=20, time_window=20)

    def _make_request(self, method, url, params=None):
        if not self.rate_limiter.allow_request():
            raise RateLimitExceeded("Rate limit exceeded")

        try:
            response = requests.request(method, url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.exceptions.RequestException as req_err:
            logger.error(f"Request error occurred: {req_err}")
            raise

        logger.info(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Text: {response.text}")

        try:
            response_dict = xmltodict.parse(response.text)

            if not isinstance(response_dict, dict):
                raise ValueError("Parsed response is not a dictionary")

            response_json = json.dumps(response_dict)
        except Exception as e:
            logger.error(f"Error parsing XML or converting to JSON: {e}")
            raise LastFMError(f"Error processing response: {e}")

        return response_json

    def _parse_response(self, response_json, *keys):
        try:
            response_dict = json.loads(response_json)
            
            
            if 'lfm' in response_dict and 'error' in response_dict['lfm']:
                error_code = response_dict['lfm']['error']['#text']
                if error_code == '2':
                    raise InvalidAPIKey("Invalid API Key")
                elif error_code == '6':
                    raise ArtistNotFoundError("Artist not found")
                elif error_code == '9':
                    raise AlbumNotFoundError("Album not found")
                elif error_code == '10':
                    raise TrackNotFoundError("Track not found")
                else:
                    raise LastFMError(f"LastFM Error: {error_code}")

            
            data = response_dict
            for key in keys:
                data = data.get(key, {})
            if not data:
                raise LastFMError("Information not found in the response")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            raise LastFMError(f"Error processing response: {e}")

    def get_track(self, track_name, artist_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'track.getinfo',
            'track': track_name,
            'artist': artist_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        track_info = self._parse_response(response_json, 'lfm', 'track')
        return Track(**track_info)

    def get_user(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getinfo',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        user_info = self._parse_response(response_json, 'lfm', 'user')
        return User(**user_info)

    def get_top_artists(self, user_name, period="overall"):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.gettopartists',
            'user': user_name,
            'api_key': self.api_key,
            'period': period,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        top_artists_info = self._parse_response(response_json, 'lfm', 'topartists', 'artist')
        return [Artist(**artist) for artist in top_artists_info]

    def get_top_albums(self, user_name, period="overall"):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.gettopalbums',
            'user': user_name,
            'api_key': self.api_key,
            'period': period,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        top_albums_info = self._parse_response(response_json, 'lfm', 'topalbums', 'album')
        return [Album(**album) for album in top_albums_info]

    def get_top_tracks(self, user_name, period="overall"):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.gettoptracks',
            'user': user_name,
            'api_key': self.api_key,
            'period': period,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        top_tracks_info = self._parse_response(response_json, 'lfm', 'toptracks', 'track')
        return [Track(**track) for track in top_tracks_info]

    def get_friends(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getfriends',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        friends_info = self._parse_response(response_json, 'lfm', 'friends', 'user')
        return [User(**friend) for friend in friends_info]

    def get_neighbours(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getneighbours',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        neighbours_info = self._parse_response(response_json, 'lfm', 'neighbours', 'user')
        return [User(**neighbour) for neighbour in neighbours_info]

    def get_now_playing(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getnowplaying',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        now_playing_info = self._parse_response(response_json, 'lfm', 'nowplaying', 'track')
        return Track(**now_playing_info) if now_playing_info else None

    def get_recent_tracks(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getrecenttracks',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        recent_tracks_info = self._parse_response(response_json, 'lfm', 'recenttracks', 'track')
        return [Track(**track) for track in recent_tracks_info]

    def get_loved_tracks(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getlovedtracks',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        loved_tracks_info = self._parse_response(response_json, 'lfm', 'lovedtracks', 'track')
        return [Track(**track) for track in loved_tracks_info]

    def get_attended_events(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getattendedevents',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        attended_events_info = self._parse_response(response_json, 'lfm', 'attendedevents', 'event')
        return [Event(**event) for event in attended_events_info]

    def get_shouts(self, user_name):
        url = "https://ws.audioscrobbler.com/2.0/"
        params = {
            'method': 'user.getshouts',
            'user': user_name,
            'api_key': self.api_key,
            'format': 'xml'
        }
        response_json = self._make_request('GET', url, params)
        shouts_info = self._parse_response(response_json, 'lfm', 'shouts', 'shout')
        return [Shout(**shout) for shout in shouts_info]
