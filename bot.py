from pyrogram import Client, filters
from pyrogram.types import Message
import os
import subprocess

API_ID = "21970746"
API_HASH = "32deb816dc3874e871b6158673fd3683"
BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"
YOUTUBE_API_KEY = "AIzaSyDcyx29y2SL8Fr0Y6l_gOBMw0YHO9KV1nU"
CHANNEL_ID = "UCy6J6n_IfRethp32skMk5rQ"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("upload_video") & filters.private)
async def upload_video_command(client, message):
    # Check if a video is attached
    if not message.video:
        await message.reply("Please attach a video file.")
        return
    
    # Download the video
    video_path = await message.download()
    
    # Prepare the command to upload the video to YouTube
    command = [
        "youtube-upload",
        "--client-secrets=client_secrets.json",
        "--title=Telegram Video",
        "--privacy=public",
        "--category=22",
        "--tags=Telegram,Pyrogram",
        "--description=Uploaded from Telegram using Pyrogram",
        video_path
    ]
    
    # Execute the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    # Check if the video was uploaded successfully
    if "Video id" in output.decode():
        video_id = output.decode().split("Video id ")[1].strip()
        video_url = f"https://youtube.com/watch?v={video_id}"
        await message.reply(f"Video uploaded successfully!\nYou can watch it [here]({video_url}).", disable_web_page_preview=True)
    else:
        await message.reply("Failed to upload video to YouTube.")

    # Clean up the downloaded video file
    os.remove(video_path)


# Start the bot
app.run()

