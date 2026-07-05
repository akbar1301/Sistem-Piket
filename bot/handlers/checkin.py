from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

from bot import config
from bot.db import repository
from bot.services.geofence import haversine_m, is_in_radius
from bot.services.time_window import day_name_indonesia, get_shift_window_for_time, determine_timeliness, now_jakarta

PHOTO, LOCATION = range(2)


async def checkin_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = repository.get_user_by_telegram(update.effective_user.id)
    if not user:
        await update.message.reply_text('Anda belum terdaftar. Gunakan /daftar {kode} terlebih dahulu.')
        return ConversationHandler.END

    if repository.get_active_session(user['uid']):
        await update.message.reply_text('Anda masih memiliki sesi piket yang berlangsung. Selesaikan atau tunggu sampai selesai.')
        return ConversationHandler.END

    now = now_jakarta()
    user_shift = f"{user['hari']} {user['shift']}"
    shift_window = get_shift_window_for_time(now)
    if not shift_window:
        await update.message.reply_text('Saat ini bukan jam piket yang sesuai. Coba lagi saat jadwalmu aktif.')
        return ConversationHandler.END

    current_shift_name, start_dt, end_dt = shift_window
    if user['hari'] != day_name_indonesia(now) or user['shift'] != current_shift_name:
        await update.message.reply_text(
            f'Ini bukan jadwal piketmu. Jadwalmu adalah {user_shift}. Kalau ini piket pengganti, minta admin approve lewat /gantiPiket.'
        )
        return ConversationHandler.END

    context.user_data['uid'] = user['uid']
    context.user_data['shift_name'] = current_shift_name
    context.user_data['window_end'] = end_dt
    await update.message.reply_text('Kirim foto di dalam ruang sekre sebagai bukti pembukaan sesi piket.')
    return PHOTO


async def photo_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.photo:
        await update.message.reply_text('Harap kirim foto, bukan teks.')
        return PHOTO
    context.user_data['foto_file_id'] = update.message.photo[-1].file_id
    await update.message.reply_text('Sekarang bagikan Live Location selama 1 jam untuk memulai sesi piket. Tetap berada di dalam ruang sekre.')
    return LOCATION


async def location_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.location:
        await update.message.reply_text('Harap bagikan Live Location.')
        return LOCATION

    loc = update.message.location
    now = now_jakarta()
    distance_m = haversine_m(loc.latitude, loc.longitude, config.SEKRE_LAT, config.SEKRE_LON)
    within = is_in_radius(distance_m, loc.horizontal_accuracy, config.RADIUS_METER)
    tepat_waktu = determine_timeliness(now, context.user_data['window_end'])
    session_id = repository.create_session(
        uid=context.user_data['uid'],
        tanggal=now.date(),
        shift_name=context.user_data['shift_name'],
        waktu_mulai=now,
        target_selesai=now + timedelta(hours=1),
        tepat_waktu=tepat_waktu,
        foto_file_id=context.user_data['foto_file_id'],
    )
    repository.log_location(session_id, now, loc.latitude, loc.longitude, loc.horizontal_accuracy, distance_m, within)
    await update.message.reply_text(
        f'Sesi piket dimulai. Status: {"tepat waktu" if tepat_waktu else "terlambat"}. '
        f'Jarak dari sekre: {distance_m:.1f} m.'
    )
    context.user_data.clear()
    return ConversationHandler.END


checkin_handlers = [
    MessageHandler(filters.PHOTO, photo_received),
    MessageHandler(filters.LOCATION, location_received),
]
