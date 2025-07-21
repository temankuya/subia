import asyncio
from pyrogram import idle
from bot import Bot

async def main():
    bot = Bot()
    await bot.start()
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
