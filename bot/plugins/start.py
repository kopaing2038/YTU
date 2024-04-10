from pyrogram import filters as Filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from ..translations import Messages as tr
from ..config import Config
from ..utubebot import UtubeBot


from pyrogram.types import ChatActionTyping

@UtubeBot.on_message(
    Filters.private
    & Filters.incoming
    & Filters.command("start")
    & Filters.user(Config.AUTH_USERS)
)
async def _start(c: UtubeBot, m: Message):
    await c.send_chat_action(m.chat.id, action=ChatActionTyping())
    await m.reply_text(
        text=tr.START_MSG.format(m.from_user.first_name),
        quote=True,
        disable_web_page_preview=True,
    )
