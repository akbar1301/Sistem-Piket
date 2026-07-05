from telegram import Update
from telegram.ext import ContextTypes

from bot.db import repository


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    user = repository.get_user_by_telegram(telegram_id)
    if not user:
        await update.message.reply_text(
            'Kamu belum terdaftar di sistem piket. Minta kode pendaftaran ke admin, lalu jalankan /daftar {kode}.'
        )
        return
    message = f"Halo {user['nama']}! Jadwalmu: {user['hari']} {user['shift']}."
    if user['utang']:
        message += f"\nYou masih memiliki utang piket sebanyak {user['utang']} sesi."
    await update.message.reply_text(message)
