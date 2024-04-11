
import os
from pytube import YouTube
from pyrogram import Client, filters




YOUTUBE_API_KEY = 'AIzaSyAqY869WGpWfSBKGdvLJWlbd8YkreNym30'
YOUTUBE_CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'


API_ID = '21970746'
API_HASH = '32deb816dc3874e871b6158673fd3683'
BOT_TOKEN = '7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4'


@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! Send me a video file and I will upload it to the YouTube channel.")

# Function to handle video messages
@Client.on_message(filters.video)
async def handle_video(client, message):
    # Get video file
    video_path = await message.download()

    # Upload video to YouTube
    youtube = YouTube(video_path)
    youtube.upload(title="Uploaded from Telegram Bot", description="Video uploaded by Telegram Bot", 
                   privacy="public", tags=["telegram", "bot"])

    # Send confirmation message
    await message.reply_text("Video uploaded to YouTube successfully!")

    # Delete video file
    os.remove(video_path)

# Function to handle unknown commands
@Client.on_message(~filters.command)
async def unknown_command(client, message):
    await message.reply_text("Sorry, I didn't understand that command.")

# Initialize the Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Run the bot
app.run()
