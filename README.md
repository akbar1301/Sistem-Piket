# Bot Telegram Verifikasi Piket

## Setup
1. Buat virtual environment Python 3.11+.
2. Install dependensi: `pip install -r requirements.txt`.
3. Salin `.env.example` menjadi `.env` lalu isi `BOT_TOKEN` dan koordinat sekre.
4. Jalankan migrasi awal:
   `python -m bot.db.migrate_from_xlsx`
5. Jalankan bot:
   `python -m bot.main`

## Migrasi awal
- File Excel sumber: `Database Piket.xlsx`
- Hasil migrasi: `data/piket.db` dan `kode_daftar_export.csv`

## Mendapatkan koordinat sekre
- Gunakan Google Maps, klik kanan titik ruang sekre, lalu salin latitude/longitude.

## Menambah admin
- Tambahkan ID Telegram ke `ADMIN_TELEGRAM_IDS` di `.env`.

## Catatan webhook
- Versi MVP menggunakan long polling.
- Untuk skala yang lebih besar, upgrade ke webhook dengan FastAPI + python-telegram-bot.
