# Panduan Penggunaan Bot Piket

Dokumen ini menjelaskan langkah-langkah penggunaan bot dari proses deploy sampai alur bekerja sehari-hari.

## 1. Persiapan Deploy di VPS Ubuntu

### 1.1 Install dependency sistem
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git build-essential libssl-dev libffi-dev
```

### 1.2 Clone project dan install dependency Python
```bash
git clone <url-repository>
cd <folder-project>
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1.3 Siapkan file konfigurasi
Salin contoh environment:
```bash
cp .env.example .env
```

Isi nilai berikut di file `.env`:
- `BOT_TOKEN`: token bot Telegram dari BotFather
- `ADMIN_TELEGRAM_IDS`: ID admin Telegram, pisah dengan koma
- `SEKRE_LAT`: latitude titik pusat ruang sekretariat
- `SEKRE_LON`: longitude titik pusat ruang sekretariat
- `RADIUS_METER`: radius geofence dalam meter
- `GRACE_PERIOD_MENIT`: toleransi saat keluar radius
- `DURASI_PIKET_MENIT`: durasi sesi piket
- `AMBANG_TERLAMBAT_MENIT`: batas terlambat
- `DENDA_PER_ABSEN`: nominal denda per absen
- `NO_UPDATE_TIMEOUT_MENIT`: batas lokasi tidak update

Contoh isi `.env`:
```env
BOT_TOKEN=123456:ABCDEF
ADMIN_TELEGRAM_IDS=123456789,987654321
SEKRE_LAT=-7.123456
SEKRE_LON=110.123456
RADIUS_METER=18
GRACE_PERIOD_MENIT=5
DURASI_PIKET_MENIT=60
AMBANG_TERLAMBAT_MENIT=30
DENDA_PER_ABSEN=10000
NO_UPDATE_TIMEOUT_MENIT=10
```

### 1.4 Jalankan migrasi data awal
```bash
python -m bot.db.migrate_from_xlsx
```

Ini akan membuat:
- database SQLite di `data/piket.db`
- file kode pendaftaran di `kode_daftar_export.csv`

### 1.5 Jalankan bot
```bash
python -m bot.main
```

Untuk menjaga bot tetap berjalan di VPS, disarankan pakai `tmux` atau `screen`.

## 2. Mendapatkan Nilai Penting

### 2.1 Token bot Telegram
1. Buka Telegram
2. Cari `@BotFather`
3. Kirim perintah `/newbot`
4. Ikuti instruksi sampai mendapat token
5. Masukkan token ke `BOT_TOKEN`

### 2.2 ID Telegram admin
Gunakan bot seperti `@userinfobot` atau `@missrose_bot`.

Contoh:
```env
ADMIN_TELEGRAM_IDS=123456789
```

### 2.3 Koordinat pusat ruang sekre
1. Buka Google Maps
2. Cari lokasi ruang sekretariat
3. Klik kanan titik tersebut
4. Salin `latitude` dan `longitude`
5. Masukkan ke `SEKRE_LAT` dan `SEKRE_LON`

## 3. Alur Pendaftaran Akun

### 3.1 User memulai bot
User buka bot Telegram lalu kirim `/start`.

Jika belum terdaftar, bot akan memberi instruksi untuk meminta kode pendaftaran ke admin.

### 3.2 Admin membagikan kode daftar
Admin mengambil kode dari file `kode_daftar_export.csv`.

Contoh isi file:
```csv
UID,KODE_DAFTAR
HMKR-K,J6V74NEC
```

Kode ini diberikan secara manual satu per satu kepada anggota.

### 3.3 User mendaftar
User kirim perintah:
```bash
/daftar J6V74NEC
```

Jika berhasil, bot akan mengonfirmasi nama, divisi, jabatan, dan jadwal piket.

## 4. Alur Check-in Piket

### 4.1 Memulai sesi piket
User kirim perintah:
```bash
/checkin
```

Bot akan meminta dua hal:
1. Foto pembuka sesi di ruang sekre
2. Live Location

### 4.2 Syarat sesi
- Foto harus dikirim dari lokasi ruang sekre
- Live Location harus dibagikan selama sesi berlangsung
- Sistem akan mencatat jarak terhadap pusat sekre

### 4.3 Status sesi
Jika lokasi berada di dalam radius, sesi berjalan normal.
Jika keluar radius, sistem akan mencatat dan bisa membatalkan sesi sesuai aturan grace period.

## 5. Alur Selama Sesi Berlangsung

Selama sesi berjalan:
- bot memantau update live location
- setiap update dicatat ke database
- jika user keluar radius terlalu lama, sesi bisa dibatalkan
- jika tidak ada update lokasi, sistem bisa menandai sebagai berhenti sharing

## 6. Status dan Informasi User

User bisa cek status dirinya dengan:
```bash
/status
```

Bot akan menampilkan:
- nama
- jadwal piket
- utang
- trust score
- status sesi aktif bila ada

## 7. Command Admin

Admin yang terdaftar di `ADMIN_TELEGRAM_IDS` dapat memakai command berikut:

### 7.1 Menandai pembayaran utang
```bash
/lunas <telegram_id> <jumlah_piket_dibayar>
```

### 7.2 Rekap data
```bash
/rekap
```

### 7.3 Update koordinat pusat sekre
```bash
/setkoordinat <lat> <lon>
```

## 8. Kebijakan Dasar Sistem

- User yang tidak check-in pada jadwalnya bisa menambah utang
- Trust score bisa turun jika bolos atau sesi dibatalkan
- Sesi yang selesai tepat waktu memberi bonus trust score
- Sesi yang dibatalkan karena keluar radius atau lokasi berhenti akan tercatat sebagai pelanggaran

## 9. Tips Operasional

- Pastikan `.env` tidak dibagikan ke publik
- Simpan file `kode_daftar_export.csv` aman dan hanya diberikan ke admin
- Gunakan VPS yang stabil agar bot tetap online
- Jika ingin bot selalu hidup saat reboot, gunakan `systemd`

## 10. Troubleshooting Sederhana

### Bot tidak merespons
- Pastikan `BOT_TOKEN` benar
- Pastikan bot sudah berjalan di VPS
- Cek log proses berjalan

### User tidak bisa daftar
- Pastikan kode yang dimasukkan benar
- Pastikan kode belum dipakai oleh akun lain

### Check-in gagal
- Pastikan user sedang di jam jadwal piket
- Pastikan live location dibagikan dengan benar
- Pastikan koordinat pusat sekre sudah benar
