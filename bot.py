
import os
from pytube import YouTube
from pyrogram import Client, filters

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pyrogram import Client, filters


YOUTUBE_API_KEY = 'AIzaSyAqY869WGpWfSBKGdvLJWlbd8YkreNym30'
YOUTUBE_CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'


API_ID = '21970746'
API_HASH = '32deb816dc3874e871b6158673fd3683'
BOT_TOKEN = '7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4'


app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private) 
async def start_command(client, message):
    await message.reply_text("Hello! Send me a video file and I will upload it to the YouTube channel.")


# Function to handle video messages
@app.on_message(filters.private) 
async def handle_video(client, message):
    try:
        if message.video:
            # Get video file
            video_path = await message.download()

            # Upload video to YouTube
            youtube = await get_authenticated_service()
            upload_video(youtube, video_path)

            # Send confirmation message
            await message.reply_text("Video uploaded to YouTube successfully!")

            # Delete video file
            os.remove(video_path)
        else:
            await message.reply_text("Please send a video file.")
    except Exception as e:
        # If an error occurs, inform the user
        await message.reply_text(f"An error occurred: {str(e)}")

# Function to authenticate and get the YouTube service
async def get_authenticated_service():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes)
    credentials = flow.run_console()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Function to upload video to YouTube
def upload_video(youtube, file):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
          "snippet": {
            "categoryId": "22",
            "description": "Video uploaded by Telegram Bot",
            "title": "Uploaded from Telegram Bot"
          },
          "status": {
            "privacyStatus": "public"
          }
        },
        media_body=file
    )
    response = request.execute()
    print(response)


# Run the bot
app.run()
