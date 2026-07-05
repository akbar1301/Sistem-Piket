from telegram import Update
from telegram.ext import ContextTypes

from bot.db import repository
from bot.services.geofence import haversine_m, is_in_radius
from bot import config
from bot.services.time_window import now_jakarta


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.edited_message or not update.edited_message.location:
        return
    user = repository.get_user_by_telegram(update.effective_user.id)
    if not user:
        return
    session = repository.get_active_session(user['uid'])
    if not session:
        return
    loc = update.edited_message.location
    now = now_jakarta()
    distance_m = haversine_m(loc.latitude, loc.longitude, config.SEKRE_LAT, config.SEKRE_LON)
    within = is_in_radius(distance_m, loc.horizontal_accuracy, config.RADIUS_METER)
    repository.log_location(session['id'], now, loc.latitude, loc.longitude, loc.horizontal_accuracy, distance_m, within)
    if not within:
        repository.increment_out_of_radius(session['id'])
