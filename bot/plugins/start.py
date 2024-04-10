from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from ..translations import Messages as tr
from ..config import Config
from ..utubebot import UtubeBot



class ChatAction:
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return self.action

    def __eq__(self, other):
        return isinstance(other, ChatAction) and self.action == other.action

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.action)

    def to_dict(self):
        return {"action": self.action}

    @staticmethod
    def from_dict(data):
        return ChatAction(data["action"])


@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("start")
    & Filters.user(Config.AUTH_USERS)
)
async def _start(c: UtubeBot, m: Message):
    await c.send_chat_action(m.chat.id, action=ChatAction("typing"))
    await m.reply_text(
        text=tr.START_MSG.format(m.from_user.first_name),
        quote=True,
        disable_web_page_preview=True,
    )

