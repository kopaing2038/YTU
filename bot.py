

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# YouTube API credentials
YOUTUBE_API_KEY = "AIzaSyDcyx29y2SL8Fr0Y6l_gOBMw0YHO9KV1nU"
CHANNEL_ID = "UCy6J6n_IfRethp32skMk5rQ"

# Pyrogram Client
api_id = "21970746"
api_hash = "32deb816dc3874e871b6158673fd3683"
bot_token = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

from pyrogram import Client
from pyrogram.types import InputMediaVideo
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Initialize YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to upload video to YouTube
def upload_video_to_youtube(file_path, title, description):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': None,
            'categoryId': 22  # category ID for People & Blogs
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    # Upload video
    media = MediaFileUpload(file_path)
    response = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()

    video_id = response.get('id')
    return video_id

# Function to send video message to Telegram
async def send_video_message(chat_id, video_id):
    await app.send_video(chat_id, video=video_id)

# Define handler for messages
@app.on_message()
async def handle_message(client, message):
    chat_id = message.chat.id
    if message.video:
        video_title = message.caption if message.caption else "Untitled"
        video_description = "This is a video uploaded via Telegram bot."
        file_path = await message.download()
        video_id = upload_video_to_youtube(file_path, video_title, video_description)
        await send_video_message(chat_id, video_id)
        os.remove(file_path)  # Remove the downloaded file after upload

# Start the bot
app.run()

