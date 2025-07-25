#CodeXBotz #mrismanaziz

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

MAX_RETRY = 3
CANCEL_KEYWORDS = ["cancel", "batal", "stop"]


async def ask_valid_message(client: Client, user_id: int, prompt: str) -> int | None:
    for attempt in range(MAX_RETRY):
        try:
            msg = await client.ask(
                chat_id=user_id,
                text=prompt,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60,
            )

            if msg.text and msg.text.lower() in CANCEL_KEYWORDS:
                await msg.reply("❌ Dibatalkan.")
                return None

            msg_id = await get_message_id(client, msg)
            if msg_id:
                return msg_id

            await msg.reply("❗ Gagal mengambil ID pesan. Coba lagi atau kirim 'cancel' untuk batal.")
        except Exception as e:
            await client.send_message(user_id, f"⚠️ Error: {e}")
            return None

    await client.send_message(user_id, "❌ Terlalu banyak percobaan. Proses dibatalkan.")
    return None


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("batch"))
async def batch(client: Client, message: Message):
    user_id = message.from_user.id

    # 🔒 Cek apakah db_channel sudah di-set
    if not hasattr(client, "db_channel"):
        await message.reply("❗ `client.db_channel` belum diatur. Cek apakah bot sudah berhasil start dengan benar dan admin di CHANNEL_DB.")
        return

    try:
        channel_id = abs(client.db_channel.id)
    except Exception as e:
        await message.reply(f"❗ Gagal ambil ID channel.\nError: `{e}`")
        return

    # ✅ Ambil pesan pertama
    f_msg_id = await ask_valid_message(
        client,
        user_id,
        "📥 Kirim *pesan pertama* dari CHANNEL_DB atau paste link post-nya:"
    )
    if f_msg_id is None:
        return

    # ✅ Ambil pesan terakhir
    s_msg_id = await ask_valid_message(
        client,
        user_id,
        "📤 Kirim *pesan terakhir* dari CHANNEL_DB atau paste link post-nya:"
    )
    if s_msg_id is None:
        return

    # 🔗 Encode dan buat link
    string = f"get-{f_msg_id * channel_id}-{s_msg_id * channel_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔗 Bagikan Link", url=f"https://telegram.me/share/url?url={link}")]]
    )

    await message.reply_text(
        f"✅ Link Batch:\n`{link}`",
        quote=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command("genlink"))
async def link_generator(client: Client, message: Message):
    user_id = message.from_user.id

    # 🔒 Cek apakah db_channel sudah di-set
    if not hasattr(client, "db_channel"):
        await message.reply("❗ `client.db_channel` belum diatur. Cek apakah bot sudah berhasil start dengan benar dan admin di CHANNEL_DB.")
        return

    try:
        channel_id = abs(client.db_channel.id)
    except Exception as e:
        await message.reply(f"❗ Gagal ambil ID channel.\nError: `{e}`")
        return

    # ✅ Ambil satu pesan
    msg_id = await ask_valid_message(
        client,
        user_id,
        "📥 Kirim *satu pesan* dari CHANNEL_DB atau paste link post-nya:"
    )
    if msg_id is None:
        return

    base64_string = await encode(f"get-{msg_id * channel_id}")
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔗 Bagikan Link", url=f"https://telegram.me/share/url?url={link}")]]
    )

    await message.reply_text(
        f"✅ Link:\n`{link}`",
        quote=True,
        reply_markup=reply_markup
    )
