
# (c) @OwnYourBotz 


import asyncio
import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    Message,
)
from pyrogram.enums.parse_mode import ParseMode
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None


def get_media_file_name_raw(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return media.file_name
    return None


@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def private_receive_handler(c: Client, m: Message):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New user joined.\n\nName: [{m.from_user.first_name}](tg://user?id={m.from_user.id}) started the bot."
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="__Sorry, you are banned from using me.__\n\n**Contact developer @OwnYourBotz for help.**",
                    parse_mode=ParseMode.MARKDOWN,
                    link_preview_options=LinkPreviewOptions(is_disabled=True)
                )
                return
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>Join my updates channel to use me 🔐</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [[ InlineKeyboardButton("Join now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}") ]]
                ),
                parse_mode=ParseMode.HTML
            )
            return
        except Exception:
            await c.send_message(
                chat_id=m.chat.id,
                text="**Something went wrong. Contact my admin @OwnYourBotz**",
                parse_mode=ParseMode.MARKDOWN,
                link_preview_options=LinkPreviewOptions(is_disabled=True))
            return
    try:
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
        file_name_encoded = get_media_file_name(m)
        file_name_display = get_media_file_name_raw(m) or "Unknown file"
        file_size = humanbytes(get_media_file_size(m))
        stream_link = "https://{}/{}/{}".format(Var.FQDN, log_msg.id, file_name_encoded) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                    Var.PORT,
                                    log_msg.id,
                                    file_name_encoded)

        msg_text = (
            "<b>Your link is ready!</b>\n\n"
            "<b>File:</b> <code>{}</code>\n\n"
            "<b>Size:</b> <code>{}</code>\n\n"
            "<b>Download:</b> {}\n\n"
            "<b>Note:</b> Link Validity: 24 Hours.\n\n"
            "<i>Powered by @OwnYourBotz</i>"
        )

        await log_msg.reply_text(
            text=(
                f"**Requested by:** [{m.from_user.first_name}]"
                f"(tg://user?id={m.from_user.id})\n"
                f"**User ID:** `{m.from_user.id}`\n"
                f"**Download link:** {stream_link}"
            ),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
        )
        await m.reply_text(
            text=msg_text.format(file_name_display, file_size, stream_link),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open download link", url=stream_link)]]),
            quote=True
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.value)}s")
        await asyncio.sleep(e.value)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Got FloodWait of {str(e.value)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**User ID:** `{str(m.from_user.id)}`", link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=ParseMode.MARKDOWN)


@StreamBot.on_message(filters.channel & (filters.document | filters.video), group=-1)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = "https://{}/{}".format(Var.FQDN, log_msg.id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                    Var.PORT,
                                    log_msg.id)
        await log_msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**Channel ID:** `{broadcast.chat.id}`\n**Request URL:** https://t.me/{(await bot.get_me()).username}?start=PredatorHackerzZ_{str(log_msg.id)}",
            # text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** https://t.me/TeleRoid_File2link_bot?start=OwnYourBotz_{str(log_msg.id)}",
            quote=True,
            parse_mode=ParseMode.MARKDOWN
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Download link 📥", url=f"https://t.me/{(await bot.get_me()).username}?start=PredatorHackerzZ_{str(log_msg.id)}")]])
            # [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=f"https://t.me/TeleRoid_File2link_bot?start=OwnYourBotz_{str(log_msg.id)}")]])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.value)}s")
        await asyncio.sleep(w.value)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Got FloodWait of {str(w.value)}s from {broadcast.chat.title}\n\n**Channel ID:** `{str(broadcast.chat.id)}`",
                             link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#error_traceback:** `{e}`", link_preview_options=LinkPreviewOptions(is_disabled=True), parse_mode=ParseMode.MARKDOWN)
        print(f"Can't edit broadcast message. Error: {e}")
