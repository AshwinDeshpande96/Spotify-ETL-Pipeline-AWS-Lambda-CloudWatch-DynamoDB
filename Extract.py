import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import creds


class SpotifyExtractor:
    client_credentials_manager = SpotifyClientCredentials(client_id=creds.cid, client_secret=creds.secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_tracks(self, uri):
        return self.sp.playlist_tracks(playlist_id=uri)
