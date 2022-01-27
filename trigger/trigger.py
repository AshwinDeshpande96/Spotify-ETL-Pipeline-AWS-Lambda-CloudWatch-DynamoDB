#!/usr/bin/python3
import sys

import pandas as pd
import requests

endpoint = "https://bslloylqzf.execute-api.us-east-2.amazonaws.com/test/spotify"
filepath = sys.argv[1]
playlists = pd.read_csv(filepath)

for (index, (playlist_id, request_sent, response)) in playlists.iterrows():
    if not request_sent:
        request_url = f"{endpoint}?playlist_id={playlist_id}"
        server_response = requests.get(request_url)
        playlists.loc[index, "response"] = server_response.text
        playlists.loc[index, "request_sent"] = True

playlists.to_csv(filepath, index=False)
