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
YOUTUBE_CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'


# Telegram API credentials
api_id = "21970746"
api_hash = "32deb816dc3874e871b6158673fd3683"
bot_token = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"


# Google OAuth 2.0 credentials
google_client_id = "298717439916-cek7ibrb563mju3u0p5c068q4bp4d34k.apps.googleusercontent.com"
google_client_secret = "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"
redirect_uri = "https://youtube.com"  # Replace with your actual redirect URI

# Google API credentials
credentials = service_account.Credentials.from_service_account_file('credentials.json')
youtube = build('youtube', 'v3', credentials=credentials)

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Handler for the "/upload" command
@app.on_message(filters.command("upload", prefixes="/") & filters.private)
async def upload_video_to_youtube(client, message: Message):
    # Check if there is a video attached
    if not message.video:
        await message.reply("Please attach a video to upload.")
        return
    
    # Download the video file
    video_path = await message.download()
    
    # Extract video title
    video_title = message.caption or "Untitled Video"
    
    # Upload video to YouTube
    request_body = {
        'snippet': {
            'title': video_title,
            'description': 'Uploaded from Telegram bot',
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    insert_request = youtube.videos().insert(
        part=",".join(request_body.keys()),
        body=request_body,
        media_body=video_path
    )

    response = insert_request.execute()

    # Get the uploaded video URL
    video_url = f"https://www.youtube.com/watch?v={response['id']}"
    
    # Reply with the uploaded video URL
    await message.reply(f"Video uploaded successfully: {video_url}")

    # Cleanup - delete the downloaded video file
    os.remove(video_path)

# Start the bot
app.run()
