#!/bin/bash

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  Menjalankan Aplikasi Seblak Bujangan"
echo "========================================"
echo ""

# Cek apakah folder venv ada
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment tidak ditemukan.${NC}"
    echo "Jalankan install.sh terlebih dahulu."
    echo ""
    exit 1
fi

# Aktifkan virtual environment
echo -e "${YELLOW}[INFO] Mengaktifkan virtual environment...${NC}"
source venv/bin/activate

# Jalankan aplikasi
echo -e "${YELLOW}[INFO] Menjalankan aplikasi Seblak Bujangan...${NC}"
echo -e "${YELLOW}[INFO] Aplikasi akan terbuka di browser secara otomatis.${NC}"
echo -e "${YELLOW}[INFO] Tekan Ctrl+C untuk menghentikan aplikasi.${NC}"
echo ""

node start.js

# Deaktivasi virtual environment saat selesai
deactivate