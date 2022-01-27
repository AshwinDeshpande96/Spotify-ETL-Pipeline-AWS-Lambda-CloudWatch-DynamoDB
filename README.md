# Spotify-ETL-Pipeline-AWS-Lambda-CloudWatch-DynamoDB
ETL Pipeline that periodically triggers an AWS lambda function to extract playlist data transform to required schema and load it into No-SQL DynamoDB Database

The purpose of this project is to help understand how ETL pipelines are developed. The main focus is to gain knowledge about how different components are connected together.
There are 3 Main components of this Project:
* Trigger - Acts as the starting point of a single ETL session
  * In this project the trigger is scheduled event to start processing new data.
  * Trigger consists of three important components
    * CRON Job to schedule the event on a loop. I chose to simply run the CRON Job every minute.
      * * * * * * python3 trigger.py playlists.csv
    * Python Script [trigger.py](https://github.com/AshwinDeshpande96/Spotify-ETL-Pipeline-AWS-Lambda-DynamoDB/trigger/triiger.py). This loops through a csv that consists of a list of Playlist IDs
      * Each Playlist ID is stored along with 2 variable: **request_sent** a boolean and **response** a json string return by the lambda function.
    * playlists.csv consists of a list of playlists. The **request_sent** variable has to be set to False to trigger lambda Function.
* 
