import sys
from pyrogram import Client, enums
from config import (
    API_HASH,
    API_ID,
    CHANNEL_DB,
    FORCE_SUB_1,
    FORCE_SUB_2,
    FORCE_SUB_3,
    BOT_TOKEN,
    WORKERS,
    get_logger,
)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=WORKERS,
            plugins={"root": "plugins"},
        )
        self.LOGGER = get_logger(__name__)

    async def start(self):
        try:
            await super().start()
            me = await self.get_me()
            self.username = me.username
            self.namebot = me.first_name
            self.LOGGER.info(f"🤖 BOT_TOKEN terdeteksi! Username: @{self.username}")
        except Exception as e:
            self.LOGGER.warning(f"Gagal start bot: {e}")
            sys.exit()

        # 🚪 Cek semua channel FORCE_SUB (maksimal 3)
        force_sub_channels = [FORCE_SUB_1, FORCE_SUB_2, FORCE_SUB_3]
        for i, chat_id in enumerate(force_sub_channels, start=1):
            if chat_id:
                try:
                    info = await self.get_chat(chat_id)
                    link = info.invite_link or await self.export_chat_invite_link(chat_id)
                    setattr(self, f"invitelink{i}", link)
                    self.LOGGER.info(f"🔒 FORCE_SUB_{i} terdeteksi: {info.title} ({info.id})")
                except Exception as e:
                    self.LOGGER.warning(f"⚠️ Tidak bisa mengakses FORCE_SUB_{i}: {e}")
                    self.LOGGER.warning(
                        f"Pastikan bot (@{self.username}) adalah admin di channel {chat_id}"
                    )
                    sys.exit()

        # 🗃️ Cek CHANNEL_DB
        try:
            db_channel = await self.get_chat(CHANNEL_DB)
            self.db_channel = db_channel

            test_message = await self.send_message(
                chat_id=db_channel.id,
                text="✅ Bot Aktif di CHANNEL_DB!"
            )
            await test_message.delete()

            self.LOGGER.info(
                f"✅ CHANNEL_DB terdeteksi!\n"
                f"📌 Nama Channel: {db_channel.title}\n"
                f"🆔 Chat ID: {db_channel.id}\n"
            )

        except Exception as e:
            self.LOGGER.warning(f"❌ Gagal mengakses CHANNEL_DB: {e}")
            self.LOGGER.warning(
                f"⚠️ Pastikan bot (@{self.username}) adalah admin di channel dengan ID {CHANNEL_DB}."
            )
            sys.exit()
