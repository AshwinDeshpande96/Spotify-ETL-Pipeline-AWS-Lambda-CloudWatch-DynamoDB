import document_keys as keys
from global_var import default_response


class Transform:
    def __init__(self, dbHandler, dataCollection):
        self.dataCollection = dataCollection
        self.dbHandler = dbHandler

    def transform_artists(self, spotify_artists):
        artists_ids = []
        for artist in spotify_artists:
            artist_id = artist.get(keys.SPOTIFY_ARTIST_ID)
            if artist_id:
                artist_document = {}
                for spotify_artist_key, artist_key in zip(keys.SPOTIFY_ARTIST_KEYS, keys.ARTIST_KEYS):
                    artist_document[artist_key] = artist.get(spotify_artist_key)
                if artist_id not in self.dataCollection.artists:
                    self.dataCollection.artists[artist_id] = []
                self.dataCollection.artists[artist_id].append(artist_document)
                artists_ids.append(artist_id)
        return artists_ids

    def transform_album(self, spotify_track):
        spotify_album = spotify_track.get(keys.SPOTIFY_ALBUM, {})
        album_id = spotify_album.get(keys.SPOTIFY_ALBUM_ID)
        if album_id:
            album_document = {}
            for spotify_album_key, album_key in zip(keys.SPOTIFY_ALBUM_KEYS, keys.ALBUM_KEYS):
                album_document[album_key] = spotify_album.get(spotify_album_key)
            album_document[keys.ALBUM_ARTISTS] = self.transform_artists(
                spotify_album.get(keys.SPOTIFY_ALBUM_ARTISTS, {}))
            if album_id not in self.dataCollection.albums:
                self.dataCollection.albums[album_id] = []
            self.dataCollection.albums[album_id].append(album_document)
        return album_id

    def transform(self, playlist_id: str, info: dict):
        self.dataCollection.playlist_document[keys.PLAYLIST_ID] = playlist_id
        self.dataCollection.playlist_document[keys.PLAYLIST_URL] = f"https://open.spotify.com/playlist/{playlist_id}"
        self.dataCollection.playlist_document[keys.PLAYLIST_TRACKS] = []
        for item in info.get(keys.SPOTIFY_ITEMS):
            spotify_track = item.get(keys.SPOTIFY_TRACK, {})
            track_id = spotify_track.get(keys.SPOTIFY_TRACK_ID)
            if track_id:
                track_document = {}
                for spotify_track_key, track_key in zip(keys.SPOTIFY_TRACK_KEYS, keys.TRACK_KEYS):
                    track_document[track_key] = spotify_track.get(spotify_track_key)
                track_document[keys.TRACK_ALBUM] = self.transform_album(spotify_track)
                track_document[keys.TRACK_ARTISTS] = self.transform_artists(
                    spotify_track.get(keys.SPOTIFY_TRACK_ARTISTS, {}))
                if track_id not in self.dataCollection.tracks:
                    self.dataCollection.tracks[track_id] = []
                self.dataCollection.tracks[track_id].append(track_document)
                self.dataCollection.playlist_document[keys.PLAYLIST_TRACKS].append(track_id)
        default_response["statusCode"] = 200
        default_response["body"]["message"] = f"{playlist_id} parsed."
        print(f"{playlist_id} parsed.")
