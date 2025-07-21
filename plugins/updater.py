#mrismanaziz

import os
import sys
from os import environ, execle, system

from git import Repo
from git.exc import InvalidGitRepositoryError
from pyrogram import filters
from pyrogram.types import Message

from bot import Bot
from config import ADMINS, LOGGER


def get_remote(repo):
    for remote_name in ["upstream", "origin"]:
        try:
            remote = repo.remotes[remote_name]
            url = remote.config_reader.get("url")
            return remote_name, url.rstrip(".git")
        except Exception:
            continue
    return None, None


def gen_chlog(repo, diff, up_repo):
    ac_br = repo.active_branch.name
    ch_log = ""
    tldr_log = ""
    ch = f"Update untuk <a href={up_repo}/tree/{ac_br}>[{ac_br}]</a>:"
    ch_tl = f"Updates untuk {ac_br}:"
    d_form = "%d/%m/%y | %H:%M"
    for i, c in enumerate(repo.iter_commits(diff), start=1):
        ch_log += (
            f"\n{i}. [{c.committed_datetime.strftime(d_form)}]\n"
            f"<a href={up_repo.rstrip('/')}/commit/{c.hexsha}>[{c.summary}]</a> — {c.author}"
        )
        tldr_log += f"\n{i}. [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] — {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return "", ""


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        return False, "", ""

    remote_name, remote_url = get_remote(repo)
    if not remote_name:
        return False, "", ""

    ac_br = repo.active_branch.name
    diff_range = f"HEAD..{remote_name}/{ac_br}"
    repo.remotes[remote_name].fetch(ac_br)
    changelog, tldr = gen_chlog(repo, diff_range, remote_url)
    return bool(changelog), changelog, tldr


@Bot.on_message(filters.command("update") & filters.user(ADMINS))
async def update_bot(_, message: Message):
    msg = await message.reply_text("🔄 Mengecek update...")
    has_update, changelog, _ = updater()

    if not has_update:
        return await msg.edit("✅ Bot sudah versi terbaru.")

    await msg.edit(f"🔔 Pembaruan Tersedia!\n{changelog}\n\nMengupdate...")

    try:
        system("git reset --hard")
        system("git pull --rebase -f")
        system("pip3 install --no-cache-dir -r requirements.txt")
    except Exception as e:
        return await msg.edit(f"❌ Gagal saat update: {e}")

    await msg.edit("✅ Update berhasil! Bot akan restart...")
    LOGGER(__name__).info("Bot updated via /update command.")
    execle(sys.executable, sys.executable, "main.py", environ)


@Bot.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(_, message: Message):
    msg = await message.reply_text("🔁 Merestart bot...")
    LOGGER(__name__).info("Bot restarting via /restart command.")
    await msg.edit("♻️ Restarting...")
    os.execle(sys.executable, sys.executable, "main.py", environ)
