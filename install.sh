#!/bin/bash
# Script untuk instalasi aplikasi Seblak Bujangan pada macOS dan Linux

echo "========================================"
echo "  Instalasi Aplikasi Seblak Bujangan"
echo "========================================"
echo ""

# Cek ketersediaan Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python tidak terdeteksi di sistem Anda."
    echo "Silakan install Python 3.7 atau lebih baru."
    echo ""
    exit 1
fi

# Cek ketersediaan Node.js
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js tidak terdeteksi di sistem Anda."
    echo "Silakan install Node.js dari https://nodejs.org/"
    echo ""
    exit 1
fi

echo "[INFO] Python dan Node.js terdeteksi. Melanjutkan instalasi..."
echo ""

# Membuat virtual environment
echo "[PROSES] Membuat virtual environment Python..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal membuat virtual environment."
    echo "Coba install virtualenv terlebih dahulu dengan: pip3 install virtualenv"
    echo ""
    exit 1
fi

# Aktifkan virtual environment
echo "[PROSES] Mengaktifkan virtual environment..."
source venv/bin/activate

# Install dependencies Python
echo "[PROSES] Menginstall dependencies Python..."
pip install streamlit pandas numpy plotly python-dateutil
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal menginstall dependencies Python."
    echo ""
    exit 1
fi

# Install dependencies Node.js
echo "[PROSES] Menginstall dependencies Node.js..."
npm install
if [ $? -ne 0 ]; then
    echo "[ERROR] Gagal menginstall dependencies Node.js."
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "  Instalasi Selesai!"
echo "========================================"
echo ""
echo "Untuk menjalankan aplikasi:"
echo "1. Buka Terminal di folder ini"
echo "2. Jalankan perintah: ./run.sh"
echo ""

# Buat run.sh executable
chmod +x run.sh

# Deaktivasi virtual environment
deactivate

echo "Tekan Enter untuk keluar..."
read