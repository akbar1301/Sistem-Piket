import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / '.env')

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
ADMIN_TELEGRAM_IDS = [int(item) for item in os.getenv('ADMIN_TELEGRAM_IDS', '').split(',') if item.strip()]

SEKRE_LAT = float(os.getenv('SEKRE_LAT', '-7.0'))
SEKRE_LON = float(os.getenv('SEKRE_LON', '110.0'))
RADIUS_METER = float(os.getenv('RADIUS_METER', '18'))
GRACE_PERIOD_MENIT = int(os.getenv('GRACE_PERIOD_MENIT', '5'))
DURASI_PIKET_MENIT = int(os.getenv('DURASI_PIKET_MENIT', '60'))
AMBANG_TERLAMBAT_MENIT = int(os.getenv('AMBANG_TERLAMBAT_MENIT', '30'))
NO_UPDATE_TIMEOUT_MENIT = int(os.getenv('NO_UPDATE_TIMEOUT_MENIT', '10'))
DENDA_PER_ABSEN = int(os.getenv('DENDA_PER_ABSEN', '10000'))

SHIFT_WINDOWS = {
    'PAGI': ('07:00', '10:00'),
    'SIANG': ('10:30', '13:00'),
    'SORE': ('13:30', '18:00'),
}

DB_PATH = BASE_DIR / 'data' / 'piket.db'
MEDIA_ROOT = BASE_DIR / 'media' / 'foto_piket'
