import os
import time
import random
from pyrogram import Client, filters
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload



YOUTUBE_API_KEY = 'AIzaSyAqY869WGpWfSBKGdvLJWlbd8YkreNym30'
YOUTUBE_CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'


API_ID = '21970746'
API_HASH = '32deb816dc3874e871b6158673fd3683'
BOT_TOKEN = '7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4'


app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Function to handle the /start command
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

            # Initialize YouTube object to get video metadata
            youtube = YouTube(video_path)
            video = youtube.streams.first()

            # Build YouTube service
            youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

            # Prepare video metadata
            request_body = {
                'snippet': {
                    'title': 'Uploaded from Telegram Bot',
                    'description': 'Video uploaded by Telegram Bot',
                    'tags': ['telegram', 'bot'],
                    'categoryId': 22  # Category ID for People & Blogs
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }

            # Upload video to YouTube with rate limiting
            while True:
                try:
                    media_file = MediaFileUpload(video_path)
                    response = youtube_service.videos().insert(
                        part='snippet,status',
                        body=request_body,
                        media_body=media_file
                    ).execute()
                    break
                except Exception as e:
                    if '429' in str(e):
                        # If rate limit exceeded, wait for some time and retry
                        delay = random.randint(10, 30)  # Random delay between 10 and 30 seconds
                        await message.reply_text(f"Rate limit exceeded. Retrying after {delay} seconds...")
                        time.sleep(delay)
                    else:
                        raise

            # Send confirmation message
            await message.reply_text("Video uploaded to YouTube successfully!")

            # Delete video file
            os.remove(video_path)
        else:
            await message.reply_text("Please send a video file.")
    except Exception as e:
        # If an error occurs, inform the user
        await message.reply_text(f"An error occurred: {str(e)}")

# Run the bot
app.run()
