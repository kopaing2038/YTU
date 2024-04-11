from pyrogram import Client, filters
from pyrogram.types import Message
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import socket

# Define your YouTube API credentials
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRET_FILE = 'client_secret.json'  # Path to your client secret file
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Define your Telegram bot token and YouTube channel ID
API_ID = "21970746"
API_HASH = "32deb816dc3874e871b6158673fd3683"
BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"
CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'  # Your YouTube channel ID

# Initialize Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Authenticate YouTube API
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
flow.redirect_uri = 'http://localhost:{}/'.format(8080)
authorization_url, _ = flow.authorization_url(access_type='offline')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8080))
sock.listen(1)

# Open a browser to the authorization URL
print("Please go to this URL and authorize access: {}".format(authorization_url))

# Wait for the authorization response
connection, client_address = sock.accept()
data = connection.recv(1024)
connection.close()
sock.close()
flow.fetch_token(code=data.decode('utf-8'))

youtube = build(API_SERVICE_NAME, API_VERSION, credentials=flow.credentials)

# Define command to handle uploading video
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
