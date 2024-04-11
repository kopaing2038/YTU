

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

# Authenticate and create YouTube service
def get_authenticated_service():
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

def upload_video_to_youtube(file_path, title, description):
    youtube = get_authenticated_service()
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': None,
            'categoryId': 22
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    media = MediaFileUpload(file_path)
    response_upload = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()
    video_id = response_upload.get('id')
    if video_id:
        request_body = {
            'snippet': {
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                },
                'position': 0
            }
        }
        response_playlist = youtube.playlistItems().insert(
            part='snippet',
            body=request_body
        ).execute()

@app.on_message()
def upload_video(bot, message: Message):
    file_id = message.video.file_id
    file_path = bot.download_media(file_id)
    title = "Your video title"
    description = "Your video description"
    try:
        upload_video_to_youtube(file_path, title, description)
        message.reply_text("Video uploaded successfully to YouTube!")
    except Exception as e:
        message.reply_text(f"Error uploading video: {str(e)}")

app.run()
