import os
import random
import asyncio
import logging
from typing import Optional, Tuple
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

from ..youtube import GoogleAuth, YouTube
from ..config import Config

log = logging.getLogger(__name__)

class Uploader:
    def __init__(self, file: str, title: Optional[str] = None):
        self.file = file
        self.title = title
        self.video_category = {
            1: "Film & Animation",
            2: "Autos & Vehicles",
            10: "Music",
            15: "Pets & Animal",
            17: "Sports",
            19: "Travel & Events",
            20: "Gaming",
            22: "People & Blogs",
            23: "Comedy",
            24: "Entertainment",
            25: "News & Politics",
            26: "Howto & Style",
            27: "Education",
            28: "Science & Technology",
            29: "Nonprofits & Activism",
        }
    async def start(self, progress: callable = None, *args) -> Tuple[bool, str]:
        self.progress = progress
        self.args = args
        await self._upload()
        return self.status, self.message

    async def _upload(self) -> None:
        try:
            loop = asyncio.get_running_loop()
            auth = GoogleAuth(Config.CLIENT_ID, Config.CLIENT_SECRET)
            if not os.path.isfile(Config.CRED_FILE):
                log.debug(f"{Config.CRED_FILE} does not exist")
                self.status = False
                self.message = "Upload failed because you did not authenticate me."
                return

            auth.LoadCredentialsFile(Config.CRED_FILE)
            google = await loop.run_in_executor(None, auth.authorize)
            categoryId = Config.VIDEO_CATEGORY if Config.VIDEO_CATEGORY and Config.VIDEO_CATEGORY in self.video_category else random.choice(list(self.video_category))

            categoryName = self.video_category[categoryId]
            title = self.title if self.title else os.path.basename(self.file)
            title = (Config.VIDEO_TITLE_PREFIX + title + Config.VIDEO_TITLE_SUFFIX).replace("<", "").replace(">", "")[:100]
            description = (Config.VIDEO_DESCRIPTION + "\nUploaded to YouTube with https://tx.me/youtubeitbot")[:5000]
            privacyStatus = Config.UPLOAD_MODE if Config.UPLOAD_MODE else "private"

            properties = dict(
                title=title,
                description=description,
                category=categoryId,
                privacyStatus=privacyStatus,
            )

            log.debug(f"payload for {self.file} : {properties}")
            youtube = YouTube(google)
            r = await loop.run_in_executor(None, youtube.upload_video, self.file, properties)
            video_id = r["id"]
            self.status = True
            self.message = f"[{title}](https://youtu.be/{video_id}) uploaded to YouTube under category {categoryId} ({categoryName})"
        except RefreshError:
            log.error("Failed to refresh access token. Check your credentials file.")
            self.status = False
            self.message = "Failed to refresh access token. Check your credentials file."
        except HttpError as e:
            if e.resp.status == 403 and "quotaExceeded" in str(e):
                log.error("Quota exceeded. Please try again later.")
                self.status = False
                self.message = "Quota exceeded. Please try again later."
            else:
                log.error(f"HTTP error occurred: {e}")
                self.status = False
                self.message = f"HTTP error occurred: {e}"
        except Exception as e:
            log.error(f"Error occurred during upload: {e}", exc_info=True)
            self.status = False
            self.message = f"Error occurred during upload: {e}"

