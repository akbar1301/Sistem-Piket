from bot.services.geofence import haversine_m, is_in_radius
from bot.services.time_window import determine_timeliness
from bot.db import repository


def test_haversine_m_basic():
    assert haversine_m(0.0, 0.0, 0.0, 0.0) == 0.0


def test_is_in_radius_accounts_for_accuracy():
    assert is_in_radius(10.0, 5.0, 15.0) is True
    assert is_in_radius(10.0, 5.0, 4.0) is False


def test_determine_timeliness_uses_threshold():
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo

    start = datetime(2024, 1, 1, 8, 0, tzinfo=ZoneInfo('Asia/Jakarta'))
    end = start + timedelta(minutes=20)
    assert determine_timeliness(start, end, 30) is False
    assert determine_timeliness(start, start + timedelta(minutes=60), 30) is True


def test_registration_code_lookup(monkeypatch):
    import sqlite3
    from bot import config
    from bot.db.models import init_db

    init_db()
    conn = sqlite3.connect(config.DB_PATH)
    conn.execute('DELETE FROM users')
    conn.execute('INSERT INTO users (uid, kode_daftar, nama, divisi, jabatan, hari, shift) VALUES (?, ?, ?, ?, ?, ?, ?)', ('U1', 'ABC12345', 'Test', 'Div', 'Staff', 'SENIN', 'PAGI'))
    conn.commit()
    conn.close()

    user = repository.get_user_by_registration_code('ABC12345')
    assert user is not None
    assert user['uid'] == 'U1'
