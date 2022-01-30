# ETL Pipeline to Extract Song Data from Spotify
ETL Pipeline that extracts playlists data from Spotify and transforms to required schema in DynamoDB Database.

The purpose of this project is to help understand how ETL pipelines are developed. The main focus is to gain knowledge about how different components are connected together.
![Arhcitecture](SpotifyArchitecture.jpg)
There are 3 Main components of this Project:
## Trigger
* In this project the trigger is scheduled event to start processing new data.
* Trigger consists of three important components
  * CRON Job to schedule the event on a loop. This CRON command executes every minute.
    * \* \* \* \* \* python3 trigger.py playlists.csv
  * Python Script [trigger.py](https://github.com/AshwinDeshpande96/Spotify-ETL-Pipeline-AWS-Lambda-DynamoDB/blob/main/trigger/trigger.py). This loops through a csv that consists of a list of Playlist IDs
    * Each Playlist ID is stored along with 2 variable: **request_sent** a boolean and **response** a json string return by the lambda function.
  * [playlists.csv](https://github.com/AshwinDeshpande96/Spotify-ETL-Pipeline-AWS-Lambda-DynamoDB/blob/main/trigger/playlists.csv) consists of a list of playlists. The **request_sent** variable has to be set to False to trigger lambda Function.

## Lambda Function
### Python Code
Lambda function receives a Playlist URI in the request packet sent by the GET Request.
This URI identifies a playlist and is required fetch details about the playlist using Spotify Developer API. This URI can be found by going to desired Playlist --> Click on More Options for \<PlaylistName\> --> Share --> Hold Alt Click on Copy link to playlist/Copy Spotify URI
Spotipy python library is used to fetch data from Spotify API. API returns a JSON document consist of data on
 * Playlist
 * Tracks
 * Album
 * Artist
 As such we transform the received data such that it is stored in Playlist, Tracks, Album and Artist tables. Each Playlist in **playlist_table** consists of a list of Track IDs corresponding to a Track in **track_table**. Each Track is a part of a single Album whereas an Album can have a number of Tracks. Furtheron Track can have a number of Artists as can an album
 
 [Lambda Function](lambda_function.py) imports [Extract](Extract.py), [Transform](Transform.py) and [Load](Load.py) and runs them sequentially.
 * Extract fetches data from Spotify
 * Transform create DataCollection objects consisting of Playlist, Tracks, Album and Artist data
 * Load function connects to DynamoDB, run de-duplication and stores using boto3 library on AWS serverless DynamoDB.

 Code given in this repo is zipped and uploaded to the Lambda Function. Similarly, python library dependencies are zipped and added as a layer to the Lambda Function.
 A REST API Gateway is created such that an EC2 instance inside a secure VPC is given access to trigger the lambda event.
 Lambda Function has to be given a role with Policies that give access to DynamoDB and CloudWatch(optional)-
 
 
## Dynamo DB
 ![Database Schema](dynamo_db_Schema.png)
 The resulting tables are stored in [playlist_table](results/playlist_results.csv), [album_table](results/album_results.csv), [artist_table](results/artist_results.csv), [track_table](results/track_results.csv)
