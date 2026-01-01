import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from pyrogram.errors import UserNotParticipant
from pyrogram.enums.parse_mode import ParseMode

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

START_TEXT = """
╭──────────────────╮
│   <b>👋 Welcome {}!</b>   │
╰──────────────────╯

<b>About Me:</b>
<i>I'm a powerful Telegram file streaming bot that converts your files into direct download links.</i>

<b>What I Can Do:</b>
• Stream files directly via browser
• Generate instant download links
• Support for all file types

<b>⚠️ Important Notice:</b>
<code>Adult content is strictly prohibited and will result in permanent ban.</code>

<i>🍃 Maintained by @TeleRoidGroup</i>"""

HELP_TEXT = """
╭────────────────╮
│   <b>📚 How to Use</b>   │
╰────────────────╯

<b>For Personal Use:</b>
• Send me any file or media
• Receive instant download link
• Share the link anywhere

<b>For Channels:</b>
• Add me as admin to your channel
• I'll automatically add download buttons to posts

<b>⏱ Link Validity:</b>
<i>All generated links expire after 24 hours</i>

<b>⚠️ Warning:</b>
<code>Adult content strictly prohibited - violators will be permanently banned.</code>

<b>Need Help?</b>
Contact Developer: <a href='https://t.me/TeleRoid14'>Abhishek Kumar</a>"""

ABOUT_TEXT = """
╭──────────────╮
│   <b>⚜ About Bot</b>   │
╰──────────────╯

<b>Bot Name:</b> <code>FileStreamX</code>
<b>Version:</b> <a href='https://t.me/MoviesFlixers_DL'>3.0.1</a>
<b>Last Updated:</b> <a href='https://canvapremiumblog.vercel.app'>01 Jan 2026</a>

<b>Developer:</b> <a href='https://telegram.me/OwnYourBotz'>Abhishek Kumar</a>
<b>GitHub:</b> <a href='https://GitHub.com/MrAbhi2k3'>@MrAbhi2k3</a>

<b>Source Code:</b>
<a href='https://github.com/PredatorHackerzZ/TG-File2Link'>View on GitHub</a>

<i>Built with ❤️ for the Telegram community</i>"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()

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


@StreamBot.on_message(filters.command('start') & filters.private)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**New User Joined**\n\nUser: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nStatus: Started the bot"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<b>⛔ Access Denied</b>\n\n<i>You have been banned from using this bot.</i>\n\nFor assistance, contact: @TeleRoid14",
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(is_disabled=True)
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>🔐 Subscription Required</b>\n\n<i>Please join our updates channel to use this bot.</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Join Channel 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode=ParseMode.HTML
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>⚠️ Error Occurred</b>\n\n<i>Something went wrong. Please contact the developer:</i>\n<a href='http://t.me/TeleRoid14'>Click here for support</a>",
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(is_disabled=True))
                return
        await m.reply_text(
            text=START_TEXT.format(m.from_user.mention),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=START_BUTTONS
              )                                                                         
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<b>⛔ Access Denied</b>\n\n<i>You are banned from using this bot.</i>\n\nContact @TeleRoid14 for assistance.",
                        parse_mode=ParseMode.HTML,
                        link_preview_options=LinkPreviewOptions(is_disabled=True)
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<b>🔐 Subscription Required</b>\n\n<i>Please join our updates channel to use this bot.</i>\n\nDue to high server load, only channel subscribers can access the bot.",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")],
                         [InlineKeyboardButton("🔄 Refresh / Try Again", url=f"https://t.me/{(await b.get_me()).username}?start=PredatorHackerzZ_{usr_cmd}")
                        
                        ]]
                    ),
                    parse_mode=ParseMode.HTML
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                text="<b>⚠️ Error Occurred</b>\n\n<i>Something went wrong. Please contact support:</i>\n<a href='https://t.me/TeleRoid14'>Support Group</a>",
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True))
        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.id,
                                     file_name)

        msg_text ="""
╭────────────────────╮
│   <b>✅ Link Generated</b>   │
╰────────────────────╯

<b>📂 File Name:</b>
<code>{}</code>

<b>📦 File Size:</b>
<code>{}</code>

<b>📥 Download Link:</b>
<code>{}</code>

<b>⏱ Validity:</b> <i>24 Hours</i>

<i>🍃 Maintained by @TeleRoidGroup</i>
"""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download Now 📥", url=stream_link)]])
        )



@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=ABOUT_BUTTONS
    )


@StreamBot.on_message(filters.command('help') & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**New User Joined**\n\nUser: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\nStatus: Started the bot"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<b>⛔ Access Denied</b>\n\n<i>You are banned from using this bot. Contact the developer for assistance.</i>",
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(is_disabled=True)
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>🔐 Subscription Required</b>\n\n<i>Please join our updates channel to use this bot.</i>\n\nDue to high server load, only channel subscribers can access the bot.",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]]
                ),
                parse_mode=ParseMode.HTML
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="<b>⚠️ Error Occurred</b>\n\n<i>Something went wrong. Please contact:</i>\n<a href='https://t.me/TeleRoid14'>Abhishek Kumar</a>",
                parse_mode=ParseMode.HTML,
                link_preview_options=LinkPreviewOptions(is_disabled=True))
            return
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode=ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=HELP_BUTTONS
        )

