from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from bot import config

JAKARTA_TZ = ZoneInfo('Asia/Jakarta')


def now_jakarta() -> datetime:
    return datetime.now(JAKARTA_TZ)


def day_name_indonesia(now: datetime | None = None) -> str:
    current = now or now_jakarta()
    mapping = {
        0: 'SENIN',
        1: 'SELASA',
        2: 'RABU',
        3: 'KAMIS',
        4: 'JUMAT',
        5: 'SABTU',
        6: 'MINGGU',
    }
    return mapping[current.weekday()]


def get_shift_window_for_time(now: datetime | None = None) -> tuple[str, datetime, datetime] | None:
    current = now or now_jakarta()
    for name, (start_str, end_str) in config.SHIFT_WINDOWS.items():
        start = datetime.combine(current.date(), time.fromisoformat(start_str), tzinfo=JAKARTA_TZ)
        end = datetime.combine(current.date(), time.fromisoformat(end_str), tzinfo=JAKARTA_TZ)
        if start <= current <= end:
            return name, start, end
    return None


def determine_timeliness(start_dt: datetime, window_end: datetime, threshold_min: int | None = None) -> bool:
    threshold = threshold_min if threshold_min is not None else config.AMBANG_TERLAMBAT_MENIT
    remaining = (window_end - start_dt).total_seconds() / 60.0
    return remaining >= threshold
