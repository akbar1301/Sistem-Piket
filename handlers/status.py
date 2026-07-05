from telegram import Update
from telegram.ext import ContextTypes

from bot.db import repository


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = repository.get_user_by_telegram(update.effective_user.id)
    if not user:
        await update.message.reply_text('Anda belum terdaftar.')
        return
    session = repository.get_active_session(user['uid'])
    status_text = 'Tidak ada sesi aktif' if not session else f'Sesi aktif: {session["status"]}'
    await update.message.reply_text(
        f"Nama: {user['nama']}\n"
        f"Jadwal: {user['hari']} {user['shift']}\n"
        f"Utang: {user['utang']}\n"
        f"Trust score: {user['trust_score']}\n"
        f"{status_text}"
    )
