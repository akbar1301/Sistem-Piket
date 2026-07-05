from datetime import datetime, date

from bot.db import repository
from bot.services.time_window import now_jakarta, day_name_indonesia
from bot import config


def run_daily_missed_piket_check() -> None:
    now = now_jakarta()
    day_name = day_name_indonesia(now)
    users = repository.get_all_users_for_daily_check(day_name)
    for user in users:
        if repository.get_session_count_for_day(user['uid'], now.date()) > 0:
            continue
        repository.add_debt(user['uid'], 1)
        repository.update_trust_score(user['uid'], -15)
        repository.record_missed_piket(user['uid'], now.date())
