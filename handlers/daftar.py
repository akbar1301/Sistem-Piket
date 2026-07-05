from telegram import Update
from telegram.ext import ContextTypes

from bot.db import repository


async def daftar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) != 1:
        await update.message.reply_text('Gunakan format: /daftar {kode}')
        return

    code = args[0].strip().upper()
    user = repository.get_user_by_registration_code(code)
    if not user:
        await update.message.reply_text('Kode tidak valid. Periksa kembali atau hubungi admin.')
        return

    if user['telegram_id'] is not None and user['telegram_id'] != update.effective_user.id:
        await update.message.reply_text('Kode ini sudah digunakan. Hubungi admin jika ini kesalahan.')
        return

    repository.register_user(user['uid'], update.effective_user.id, code)
    await update.message.reply_text(
        f"Terdaftar sebagai {user['nama']} ({user['divisi']} - {user['jabatan']}).\n"
        f"Jadwal piket: {user['hari']} {user['shift']}."
    )
