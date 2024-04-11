


from pyrogram import Client, filters
from pyrogram.types import Message
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

YOUTUBE_API_KEY = "AIzaSyDcyx29y2SL8Fr0Y6l_gOBMw0YHO9KV1nU"
CHANNEL_ID = "UCy6J6n_IfRethp32skMk5rQ"

# Define scopes for YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Pyrogram bot setup
API_ID = "21970746"
API_HASH = "32deb816dc3874e871b6158673fd3683"
BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"

# Initialize Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def authenticate_youtube():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)


# Upload video to YouTube
def upload_video_to_youtube(video_file):
    youtube = authenticate_youtube()
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "Description of your video",
                "title": "Title of your video"
            },
            "status": {
                "privacyStatus": "private"  # You can change privacy status here
            }
        },
        media_body=MediaFileUpload(video_file)
    )
    response = request.execute()
    video_id = response['id']
    return video_id


# Command to upload video
@app.on_message(filters.command("upload"))
async def upload_video_command(client, message):
    if message.video:
        video_file = await message.download()
        video_id = upload_video_to_youtube(video_file)
        await message.reply_text(f"Video uploaded successfully. Video ID: {video_id}")
    else:
        await message.reply_text("Please upload a video file to upload.")


# Run the bot
app.run()
