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
<i>👋 Hello,</i>{}\n
<i>I am a Telegram file streaming bot that also creates direct download links.</i>\n
<i>Tap <b>Help</b> to learn how to use me.</i>\n
<i><u>𝗪𝗔𝗥𝗡𝗜𝗡𝗚 🚸</u></i>
<b>🔞 Adult content leads to a permanent ban.</b>\n\n
<i><b>🍃 Maintained by:</b> @TeleRoidGroup</i>"""

HELP_TEXT = """
<i>- Send me any file or media from Telegram.</i>
<i>- I will provide an external direct download link.</i>
<i>- Add me to your channel to attach Direct Download buttons to your posts.</i>
<i>- Links are fast and temporary (expire after 24 hours).</i>\n
<u>🔸 𝗪𝗔𝗥𝗡𝗜𝗡𝗚 🚸</u>\n
<b>🔞 Adult content leads to a permanent ban.</b>\n
<i>Report issues to the developer:</i> <b>: <a href='https://t.me/TeleRoid14'>[ツAʙʜɪsʜᴇᴋ Kᴜᴍᴀʀ]</a></b>"""

ABOUT_TEXT = """
<b>⚜ Name: FileStreamX</b>\n
<b>🔸 Version: <a href='https://t.me/MoviesFlixers_DL'>3.0.1</a></b>\n
<b>🔹 Source: <a href='https://github.com/PredatorHackerzZ/TG-File2Link'>Click here</a></b>\n
<b>🔸 GitHub: <a href='https://GitHub.com/MrAbhi2k3'>ツAʙʜɪsʜᴇᴋ Kᴜᴍᴀʀ</a></b>\n
<b>🔹 Developer: <a href='https://telegram.me/OwnYourBotz'>ツAʙʜɪsʜᴇᴋ Kᴜᴍᴀʀ</a></b>\n
<b>🔸 Last updated: <a href='https://canvapremiumblog.vercel.app'>01 - Jan 2026</a></b>"""

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
            link_preview_options=LinkPreviewOptions(disable_web_page_preview=True),
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            link_preview_options=LinkPreviewOptions(disable_web_page_preview=True),
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            link_preview_options=LinkPreviewOptions(disable_web_page_preview=True),
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
            f"**New User Joined:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Sorry, you are banned from using me. Contact the developer for help.__\n\n@TeleRoid14",
                        parse_mode=ParseMode.MARKDOWN,
                        link_preview_options=LinkPreviewOptions(disable_web_page_preview=True)
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Join my updates channel to use me 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("JOin Now 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode=ParseMode.HTML
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Something went wrong. Contact the developer:</i> <b><a href='http://t.me/TeleRoid14'>[ Click here ]</a></b>",
                    parse_mode=ParseMode.HTML,
                    link_preview_options=LinkPreviewOptions(disable_web_page_preview=True))
                return
        await m.reply_text(
            text=START_TEXT.format(m.from_user.mention),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(disable_web_page_preview=True),
            reply_markup=START_BUTTONS
              )                                                                         
                                                                                       
                                                                            
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="**Sorry, you are banned from using me. Contact @TeleRoid14 for assistance.**",
                        parse_mode=ParseMode.MARKDOWN,
                        link_preview_options=LinkPreviewOptions(disable_web_page_preview=True)
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Please join my updates channel to use this bot.**\n\n**Only channel subscribers can use the bot right now due to load.**",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton("🤖 Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")],
                         [InlineKeyboardButton("🔄 Refresh / Try Again", url=f"https://t.me/{(await b.get_me()).username}?start=AvishkarPatil_{usr_cmd}")
                        
                        ]]
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                text="**Something went wrong. Contact support:** [ツAʙʜɪsʜᴇᴋ Kᴜᴍᴀʀ](https://t.me/TeleRoid14)",
                parse_mode=ParseMode.MARKDOWN,
                link_preview_options=LinkPreviewOptions(disable_web_page_preview=True))
        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))
        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.id,
                                     file_name)

        msg_text ="""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 �s 𝗥𝗲𝗮𝗱ʏ</u></i>\n
<b>📂 File name :</b> <i>{}</i>\n
<b>📦 Size :</b> <i>{}</i>\n
<b>📥 Download :</b> <i>{}</i>\n
<b>🚸 Note: Links expire in 24 hours</b>\n
<i>🍃 Maintained by :</i> <b>@AvishkarPatil</b>
"""

        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode=ParseMode.HTML,
            link_preview_options=LinkPreviewOptions(disable_web_page_preview=True),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]])
        )



@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(bot, update):
    await update.reply_text(
        text=ABOUT_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )


@StreamBot.on_message(filters.command('help') & filters.private)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ **\n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Started Your Bot !!__"
        )
    if Var.UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ</i>",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs Bᴏᴛ!**\n\n__Dᴜᴇ ᴛᴏ Oᴠᴇʀʟᴏᴀᴅ, Oɴʟʏ Cʜᴀɴɴᴇʟ Sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ Bᴏᴛ!__",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton("🤖 Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]]
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="__Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍᴇ__ [ツAʙʜɪsʜᴇᴋ Kᴜᴍᴀʀ](https://t.me/Avishkarpatil).",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text=HELP_TEXT,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
        )

