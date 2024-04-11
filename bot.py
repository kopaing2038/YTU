from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess

API_ID = "21970746"
API_HASH = "32deb816dc3874e871b6158673fd3683"
BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"
YOUTUBE_API_KEY = "AIzaSyDcyx29y2SL8Fr0Y6l_gOBMw0YHO9KV1nU"
CHANNEL_ID = "UCy6J6n_IfRethp32skMk5rQ"




from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient import discovery
import httplib2
from datetime import datetime, timedelta
import pytz
from pyrogram import Client, filters



# Initialize Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def getScheduleDateTime(days=0):
    # Set the publish time to 2 PM Eastern Time (US) on the next day
    eastern_tz = pytz.timezone('America/Los_Angeles')
    publish_time = datetime.now(eastern_tz)
    if days > 0:
        publish_time = datetime.now(eastern_tz) + timedelta(days)
    publish_time = publish_time.replace(hour=14, minute=0, second=0, microsecond=0)

    # Set the publish time in the UTC timezone
    publish_time_utc = publish_time.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return publish_time_utc


# Start the OAuth flow to retrieve credentials
def authorize_credentials():
    CLIENT_SECRET = 'client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/youtube'
    STORAGE = Storage('credentials.storage')
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


def getYoutubeService():
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest')
    service = discovery.build('youtube', 'v3', http=http, discoveryServiceUrl=discoveryUrl)
    return service


def upload_video(file_path, title, description='', tags=[], privacy_status='public', day=0):
    print("Uploading...")
    youtube = getYoutubeService()
    try:
        # Define the video resource object
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }

        if privacy_status == 'private':
            body['status']['publishAt'] = getScheduleDateTime(day)

        # Define the media file object
        media_file = MediaFileUpload(file_path)

        # Call the API's videos.insert method to upload the video
        videos = youtube.videos()
        response = videos.insert(
            part='snippet,status',
            body=body,
            media_body=media_file
        ).execute()

        # Print the response after the video has been uploaded
        print('Video uploaded successfully!\n')
        print(f'Title: {response["snippet"]["title"]}')
        print(f'URL: https://www.youtube.com/watch?v={response["id"]}')

    except HttpError as e:
        # print(f'An HTTP error {error.resp.status} occurred:\n{error.content}')
        raise Exception(f"An HTTP error {e.resp.status} occurred: {e.content.decode('utf-8')}")


@app.on_message(filters.private)
def echo(client, message):
    vid_path = 'your video path'
    upload_video(vid_path, 'video title')


# Start the bot
app.run()


