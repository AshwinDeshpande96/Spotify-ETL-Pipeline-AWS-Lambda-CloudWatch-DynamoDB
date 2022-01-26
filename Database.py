import boto3

from botocore.exceptions import ClientError


class DynamoDB:
    dynamodb = boto3.resource('dynamodb')
    playlist_table = dynamodb.Table('playlist_table')

    def playlist_exists(self, uri):
        try:
            response = self.playlist_table.get_item(Key={"playlist_uri": uri})
            if "Item" in response:
                return True
            return False
        except ClientError as ce:
            print(ce.response['Error']['Message'])
            return False


class DataCollection:
    playlist_document = {}
    albums = {}
    artists = {}
    tracks = {}
