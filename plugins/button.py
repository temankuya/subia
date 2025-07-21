from config import FORCE_SUB_1, FORCE_SUB_2, FORCE_SUB_3
from pyrogram.types import InlineKeyboardButton


def get_force_sub_links(client):
    links = []
    if FORCE_SUB_1:
        links.append(("📣 Channel 1", client.invitelink))
    if FORCE_SUB_2:
        links.append(("📣 Channel 2", client.invitelink2))
    if FORCE_SUB_3:
        links.append(("📣 Channel 3", client.invitelink3))
    return links


def start_button(client):
    links = get_force_sub_links(client)
    buttons = []

    if links:
        buttons.append([InlineKeyboardButton(text="📢 Wajib Join:", callback_data="noop")])
        row = []
        for i, (text, url) in enumerate(links):
            row.append(InlineKeyboardButton(text=text, url=url))
            if len(row) == 3:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)

    buttons.append([InlineKeyboardButton(text="❓ Bantuan", callback_data="help")])
    buttons.append([InlineKeyboardButton(text="❌ Tutup", callback_data="Tutup")])
    return buttons


def fsub_button(client, message):
    links = get_force_sub_links(client)
    if not links:
        return []

    buttons = []
    buttons.append([InlineKeyboardButton(text="📢 Wajib Join:", callback_data="noop")])
    row = []
    for i, (text, url) in enumerate(links):
        row.append(InlineKeyboardButton(text=text, url=url))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    try:
        buttons.append([
            InlineKeyboardButton(
                text="🔁 Coba Lagi",
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass

    return buttons
