from spotipy.exceptions import SpotifyException

from Database import DynamoDB, DataCollection
from Extract import SpotifyExtractor
from Load import Load
from Transform import Transform
from global_var import default_response


def lambda_handler(event, context):
    if not isinstance(event, dict):
        return default_response
    if "queryStringParameters" in event and "playlist_id" in event["queryStringParameters"]:
        playlist_id = event["queryStringParameters"]["playlist_id"]
        uri = f"spotify:playlist:{playlist_id}"
    else:
        print("Playlist ID not given. Exiting.")
        default_response['statusCode'] = 404
        default_response['body']['message'] = "Playlist ID not given. Please provide a valid Playlist ID."
        return default_response
    try:
        dbHandler = DynamoDB()
        if dbHandler.playlist_exists(playlist_id):
            default_response['statusCode'] = 208
            default_response['body']['message'] = "Playlist already parsed. Please provide another Playlist ID."
            print("Playlist already parsed. Please provide another Playlist ID.")
        else:
            extractor = SpotifyExtractor()
            data_collection = DataCollection()
            transformer = Transform(dbHandler, data_collection)
            loader = Load(data_collection, dbHandler)

            info = extractor.get_tracks(uri=uri)
            transformer.transform(playlist_id, info)
            loader.load()
    except SpotifyException as spe:
        print(spe)
        print("Incorrect Playlist ID. Please provide a valid Playlist ID.")
        default_response["body"]["message"] = "Incorrect Playlist ID. Please provide a valid Playlist ID."
    return default_response
