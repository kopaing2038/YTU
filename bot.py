
import os
from pytube import YouTube
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Update, ParseMode
from telegram.ext.filters import Filters


TOKEN = '7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4'

YOUTUBE_API_KEY = 'AIzaSyAqY869WGpWfSBKGdvLJWlbd8YkreNym30'
YOUTUBE_CHANNEL_ID = 'UCy6J6n_IfRethp32skMk5rQ'

# Function to handle the /start command
def start(update, context):
    update.message.reply_text("Hello! Send me a video file and I will upload it to the YouTube channel.")

# Function to handle video messages
def handle_video(update, context):
    # Get video file
    video = update.message.video.get_file()
    video_path = video.download()

    # Upload video to YouTube
    youtube = YouTube(video_path)
    youtube.upload(title="Uploaded from Telegram Bot", description="Video uploaded by Telegram Bot", 
                   privacy="public", tags=["telegram", "bot"])

    # Send confirmation message
    update.message.reply_text("Video uploaded to YouTube successfully!")

    # Delete video file
    os.remove(video_path)

# Function to handle unknown commands
def unknown(update, context):
    update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    # Initialize the Telegram bot
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video, handle_video))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
