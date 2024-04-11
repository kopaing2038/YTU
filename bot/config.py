import os


class Config:

    BOT_TOKEN = "7191544925:AAF1wNdb4SfdbzM6-691e0eNio4EmAqkRQ4"

    SESSION_NAME = os.environ.get('SESSION', 'Media_search')
    
    API_ID = "21970746"

    API_HASH = "32deb816dc3874e871b6158673fd3683"

    CLIENT_ID = "411545135490-2fk7pcbqt28bldrosc66g7vabitc6s9u.apps.googleusercontent.com"

    CLIENT_SECRET = "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"

    BOT_OWNER = "1113630298"

    AUTH_USERS_TEXT = os.environ.get("AUTH_USERS")

    AUTH_USERS = [BOT_OWNER, 1113630298] + (
        [int(user.strip()) for user in AUTH_USERS_TEXT.split("5859405449")]
        if AUTH_USERS_TEXT
        else []
    )

    VIDEO_DESCRIPTION = (
        os.environ.get("VIDEO_DESCRIPTION", "").replace("<", "").replace(">", "")
    )

    VIDEO_CATEGORY = (
        int(os.environ.get("VIDEO_CATEGORY")) if os.environ.get("VIDEO_CATEGORY") else 0
    )

    VIDEO_TITLE_PREFIX = os.environ.get("VIDEO_TITLE_PREFIX", "hi")

    VIDEO_TITLE_SUFFIX = os.environ.get("VIDEO_TITLE_SUFFIX", "")

    DEBUG = bool(os.environ.get("DEBUG"))

    UPLOAD_MODE = os.environ.get("UPLOAD_MODE") or False
    if UPLOAD_MODE:
        if UPLOAD_MODE.lower() in ["private", "public", "unlisted"]:
            UPLOAD_MODE = UPLOAD_MODE.lower()
        else:
            UPLOAD_MODE = False

    CRED_FILE = "auth_token.txt"
