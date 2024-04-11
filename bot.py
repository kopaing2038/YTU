

from pyrogram import Client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Define your YouTube API credentials
API_KEY  = "AIzaSyDcyx29y2SL8Fr0Y6l_gOBMw0YHO9KV1nU"
CHANNEL_ID = "UCy6J6n_IfRethp32skMk5rQ"



from pyrogram import Client, filters
from pyrogram.types import Message
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Define YouTube API credentials
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


API_ID = "21970746"
API_HASH = "32deb816dc3874e871b6158673fd3683"
BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"


# Authenticate YouTube API
def authenticate_youtube():
    creds = None
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
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the command handler for /upload_video
@app.on_message(filters.command("upload_video") & filters.private)
async def upload_video_to_youtube(client, message: Message):
    # Check if the message contains a video
    if message.video:
        video_file_id = message.video.file_id
        # Download the video file
        video_path = await client.download_media(video_file_id)
        
        # Authenticate YouTube API
        youtube = authenticate_youtube()
        
        # Upload video to YouTube
        request_body = {
            'snippet': {
                'title': message.caption if message.caption else 'Untitled',
                'description': 'Uploaded using Telegram Bot',
                'tags': ['telegram', 'bot'],
                'categoryId': 20  # Specify the category ID if needed
            },
            'status': {
                'privacyStatus': 'public'  # Change privacy status if needed
            }
        }
        
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=video_path
        ).execute()
        
        video_id = response['id']
        
        # Get the URL of the uploaded video
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Send the video URL as a reply
        await message.reply_text(f'Video uploaded successfully: {video_url}')
        
        # Delete the downloaded video file
        os.remove(video_path)
    else:
        # If the message doesn't contain a video, send an error message
        await message.reply_text('Please upload a video to upload to YouTube.')

# Start the bot
app.run()

