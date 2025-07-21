# Codexbotz - Handler Link Generator
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import Bot
from config import ADMINS, CHANNEL_DB, DISABLE_BUTTON, LOGGER
from helper_func import encode

# Buffer untuk media group (album)
MEDIA_GROUP_BUFFER = {}

# Handle pesan pribadi dari admin (kecuali command)
@Bot.on_message(
    filters.private
    & filters.user(ADMINS)
    & ~filters.command([
        "start", "users", "broadcast", "ping", "uptime", "batch",
        "logs", "genlink", "update", "stats", "vars",
    ])
)
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Sedang diproses...", quote=True)
    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except Exception as e:
        LOGGER(__name__).warning(e)
        await reply_text.edit_text("❌ Terjadi kesalahan.")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Bagikan Link", url=f"https://telegram.me/share/url?url={link}")]
    ])

    await reply_text.edit(
        f"✅ Link:\n`{link}`",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    if not DISABLE_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass


# Handle post masuk di CHANNEL_DB
@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_DB))
async def new_post(client: Client, message: Message):
    if DISABLE_BUTTON:
        return

    # Deteksi media group (album)
    if message.media_group_id:
        group_id = message.media_group_id
        if group_id not in MEDIA_GROUP_BUFFER:
            MEDIA_GROUP_BUFFER[group_id] = []

        MEDIA_GROUP_BUFFER[group_id].append(message)
        await asyncio.sleep(2)  # Tunggu semua bagian media masuk

        group_messages = MEDIA_GROUP_BUFFER.pop(group_id, [])
        if not group_messages:
            return

        first_msg = group_messages[0]
        last_msg = group_messages[-1]
        channel_id = abs(client.db_channel.id)

        string = f"get-{first_msg.id * channel_id}-{last_msg.id * channel_id}"
        base64_string = await encode(string)
        link = f"https://t.me/{client.username}?start={base64_string}"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Bagikan Link", url=f"https://telegram.me/share/url?url={link}")]
        ])

        try:
            await last_msg.edit_reply_markup(reply_markup)
        except Exception:
            pass

    else:
        # Untuk post biasa (bukan album)
        converted_id = message.id * abs(client.db_channel.id)
        string = f"get-{converted_id}"
        base64_string = await encode(string)
        link = f"https://t.me/{client.username}?start={base64_string}"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Bagikan Link", url=f"https://telegram.me/share/url?url={link}")]
        ])

        try:
            await message.edit_reply_markup(reply_markup)
        except Exception:
            pass
