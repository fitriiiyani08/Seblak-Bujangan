#!/bin/bash
# Script untuk menjalankan aplikasi Seblak Bujangan pada macOS dan Linux

echo "========================================"
echo "  Menjalankan Aplikasi Seblak Bujangan"
echo "========================================"
echo ""

# Cek jika virtual environment ada
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment tidak ditemukan."
    echo "Jalankan ./install.sh terlebih dahulu."
    echo ""
    exit 1
fi

# Aktifkan virtual environment
echo "[PROSES] Mengaktifkan virtual environment..."
source venv/bin/activate

# Jalankan aplikasi menggunakan npm start
echo "[PROSES] Menjalankan aplikasi Seblak Bujangan..."
echo "Aplikasi akan terbuka di browser secara otomatis pada http://localhost:5000"
echo "Tekan Ctrl+C untuk menghentikan aplikasi."
echo ""

node start.js

# Deaktivasi virtual environment
deactivate