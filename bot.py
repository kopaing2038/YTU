import os
import time
import random
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pyrogram import Client, filters
from pyrogram.types import Message
from google.oauth2 import service_account
from pyrogram import Client, filters


YOUTUBE_API_KEY = 'AIzaSyAqY869WGpWfSBKGdvLJWlbd8YkreNym30'



# Telegram API credentials
api_id = "21970746"
api_hash = "32deb816dc3874e871b6158673fd3683"
bot_token = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"


# Google OAuth 2.0 credentials
google_client_id = "298717439916-cek7ibrb563mju3u0p5c068q4bp4d34k.apps.googleusercontent.com"
google_client_secret = "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"
redirect_uri = "https://youtube.com"  

from pyrogram import Client, filters
from pyrogram.types import Message
from pytube import YouTube
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = 'client_secret.json'  # Path to your client secret file
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

API_ID = "21970746"
API_HASH = "32deb816dc3874e871b6158673fd3683"
BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"
CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'  # Your YouTube channel ID

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("upload_video") & filters.private)
async def upload_video_to_youtube(client, message: Message):
    # Check if the message contains a video
    if message.video:
        # Download the video
        video_path = await message.download()
        
        # Get video title
        video_title = message.caption if message.caption else "Untitled"
        
        # Upload the video to YouTube
        request_body = {
            'snippet': {
                'title': video_title,
                'description': 'Uploaded using Telegram bot.'
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
        media_file = MediaFileUpload(video_path)
        youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file
        ).execute()
        
        await message.reply_text("Video uploaded to YouTube successfully!")
        
    else:
        await message.reply_text("Please send a video file to upload.")


app.run()
