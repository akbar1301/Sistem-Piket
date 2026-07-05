import asyncio
import logging
from pathlib import Path

from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from bot import config
from bot.handlers.admin import lunas, rekap, setkoordinat
from bot.handlers.checkin import PHOTO, LOCATION, checkin_start, photo_received, location_received, checkin_handlers
from bot.handlers.daftar import daftar
from bot.handlers.location_tracking import handle_location
from bot.handlers.start import start
from bot.handlers.status import status
from bot.utils.logger import get_logger

logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)


async def main() -> None:
    if not config.BOT_TOKEN:
        raise RuntimeError('BOT_TOKEN tidak ditemukan di .env')

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('daftar', daftar))
    app.add_handler(CommandHandler('status', status))
    app.add_handler(CommandHandler('lunas', lunas))
    app.add_handler(CommandHandler('rekap', rekap))
    app.add_handler(CommandHandler('setkoordinat', setkoordinat))

    checkin_conv = ConversationHandler(
        entry_points=[CommandHandler('checkin', checkin_start)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, photo_received)],
            LOCATION: [MessageHandler(filters.LOCATION, location_received)],
        },
        fallbacks=[],
        name='checkin_conv',
    )
    app.add_handler(checkin_conv)
    app.add_handler(MessageHandler(filters.LOCATION & ~filters.COMMAND, handle_location))

    await app.bot.set_my_commands([
        BotCommand('start', 'Mulai interaksi dengan bot'),
        BotCommand('daftar', 'Daftar akun dengan kode'),
        BotCommand('checkin', 'Mulai sesi piket'),
        BotCommand('status', 'Lihat status piket Anda'),
    ])
    await app.run_polling()


if __name__ == '__main__':
    asyncio.run(main())
