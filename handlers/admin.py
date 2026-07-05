from telegram import Update
from telegram.ext import ContextTypes

from bot import config
from bot.db import repository


async def admin_only(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in config.ADMIN_TELEGRAM_IDS:
        await update.message.reply_text('Anda tidak memiliki akses admin.')
        return False
    return True


async def lunas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await admin_only(update, context):
        return
    args = context.args
    if len(args) != 2:
        await update.message.reply_text('Gunakan: /lunas {telegram_id} {jumlah_piket_dibayar}')
        return
    telegram_id = int(args[0])
    amount = int(args[1])
    user = repository.get_user_by_telegram(telegram_id)
    if not user:
        await update.message.reply_text('User tidak ditemukan.')
        return
    if amount > user['utang']:
        await update.message.reply_text('Jumlah pembayaran melebihi utang saat ini.')
        return
    repository.reduce_debt(user['uid'], amount)
    await update.message.reply_text(f'Utang {user["nama"]} dikurangi sebanyak {amount}.')


async def rekap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await admin_only(update, context):
        return
    await update.message.reply_text('Fitur rekap belum diimplementasikan penuh; export Excel bisa dikembangkan lebih lanjut.')


async def setkoordinat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await admin_only(update, context):
        return
    if len(context.args) != 2:
        await update.message.reply_text('Gunakan: /setkoordinat {lat} {lon}')
        return
    repository.set_config('SEKRE_LAT', context.args[0])
    repository.set_config('SEKRE_LON', context.args[1])
    await update.message.reply_text('Koordinat sekre diperbarui.')
