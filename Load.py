from pprint import pprint

import document_keys as keys
from global_var import default_response


class Load:
    def __init__(self, dataCollection, DBHandler):
        self.DBHandler = DBHandler
        self.dataCollection = dataCollection

    def merge(self, doc1, doc2):
        doc = {}
        keys = set(list(doc1.keys()) + list(doc2.keys()))
        for key in keys:
            value1 = doc1.get(key)
            value2 = doc2.get(key)
            if value1 and not value2:
                value = value1
            elif value2 and not value1:
                value = value2
            elif value1 and value2:
                if isinstance(value1, dict):
                    value = self.merge(value1, value2)
                elif isinstance(value1, list):
                    value = list(set(value1 + value2))
                else:
                    value = value1
            else:
                value = None
            doc[key] = value
        return doc

    def deduplicate(self, table):
        for did, documents in table.items():
            document = documents[0]
            if len(documents) > 1:
                for doc in documents[1:]:
                    document = self.merge(document, doc)
            table[did] = document
        return table

    def update_table(self, table, table_name, table_id):
        table_keys = list(table.keys())
        responses = []
        for i in range(0, len(table_keys), 50):
            keychunk = table_keys[i:i + 50]
            response = self.DBHandler.dynamodb.batch_get_item(RequestItems={
                table_name: {
                    "Keys": [{table_id: tid} for tid in keychunk]
                }
            }
            )
            responses.append(response)
        for response in responses:
            if table_name in response['Responses']:
                for document in response['Responses'][table_name]:
                    db_id = document.get(table_id)
                    if db_id in table:
                        document = self.merge(document, table[db_id])
                        table[db_id] = document
        try:
            table = list(table.values())
            for i in range(0, len(table), 25):
                chunk = table[i:i + 25]
                update_response = self.DBHandler.dynamodb.batch_write_item(RequestItems={
                    table_name: [
                        {
                            "PutRequest": {
                                "Item": chunk[j]
                            }
                        }
                        for j in range(len(chunk))
                    ]
                }
                )
                pprint(update_response)
            default_response['statusCode'] = 200
            default_response['body']['message'] = "DB Update Successful"
        except Exception as e:
            pprint(e)
            default_response['statusCode'] = 400
            default_response['body']['message'] = "DB Update Unsuccessful"

    def load_to_db(self):
        playlist_response = self.DBHandler.playlist_table.put_item(Item=self.dataCollection.playlist_document)
        print(playlist_response)
        self.update_table(self.dataCollection.albums, "album_table", keys.ALBUM_ID)
        self.update_table(self.dataCollection.artists, "artist_table", keys.ARTIST_ID)
        self.update_table(self.dataCollection.tracks, "track_table", keys.TRACK_ID)

    def load(self):
        self.dataCollection.albums = self.deduplicate(self.dataCollection.albums)
        self.dataCollection.artists = self.deduplicate(self.dataCollection.artists)
        self.dataCollection.tracks = self.deduplicate(self.dataCollection.tracks)
        self.load_to_db()
