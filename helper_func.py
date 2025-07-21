import asyncio
import base64
import re

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from config import (
    ADMINS,
    FORCE_SUB_1,
    FORCE_SUB_2,
    FORCE_SUB_3,
    FORCE_SUB_4
)

FORCE_SUB_CHANNELS = [FORCE_SUB_1, FORCE_SUB_2, FORCE_SUB_3, FORCE_SUB_4]

async def is_subscribed(filter, client, update):
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True

    for channel in FORCE_SUB_CHANNELS:
        if not channel:
            continue
        try:
            member = await client.get_chat_member(chat_id=channel, user_id=user_id)
        except UserNotParticipant:
            return False
        except Exception:
            return False
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            return False
    return True


# Fungsi filter individual, tetap dipertahankan
async def _sub(filter, client, update, channel_id):
    if not channel_id:
        return True
    user_id = update.from_user.id
    if user_id in ADMINS:
        return True
    try:
        member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
    except UserNotParticipant:
        return False
    except Exception:
        return False
    return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]

# Variasi filter per channel
sub1 = filters.create(lambda f, c, u: _sub(f, c, u, FORCE_SUB_1))
sub2 = filters.create(lambda f, c, u: _sub(f, c, u, FORCE_SUB_2))
sub3 = filters.create(lambda f, c, u: _sub(f, c, u, FORCE_SUB_3))
sub4 = filters.create(lambda f, c, u: _sub(f, c, u, FORCE_SUB_4))
subs = filters.create(is_subscribed)


# Utilitas encoding/decoding
async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return base64_bytes.decode("ascii").strip("=")

async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    return base64.urlsafe_b64decode(base64_bytes).decode("ascii")


# Ambil banyak pesan dari db_channel
async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages < len(message_ids):
        temb_ids = message_ids[total_messages:total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id, message_ids=temb_ids
            )
        except BaseException:
            msgs = []
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages


# Cek ID pesan asli dari message
async def get_message_id(client, message):
    if message.forward_from_chat and message.forward_from_chat.id == client.db_channel.id:
        return message.forward_from_message_id
    elif message.forward_from_chat or message.forward_sender_name or not message.text:
        return 0
    else:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        CHANNEL_DB = matches.group(1)
        msg_id = int(matches.group(2))
        if CHANNEL_DB.isdigit():
            return msg_id if f"-100{CHANNEL_DB}" == str(client.db_channel.id) else 0
        elif CHANNEL_DB == client.db_channel.username:
            return msg_id
        return 0
