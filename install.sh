#!/bin/bash

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  Instalasi Aplikasi Seblak Bujangan"
echo "========================================"
echo ""

# Cek apakah Python terinstall
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python tidak terinstall di sistem Anda.${NC}"
    echo "Silakan install Python 3.7 atau yang lebih baru."
    echo ""
    exit 1
fi

# Cek apakah Node.js terinstall
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js tidak terinstall di sistem Anda.${NC}"
    echo "Silakan install Node.js dari https://nodejs.org/"
    echo ""
    exit 1
fi

echo -e "${GREEN}[INFO] Python dan Node.js terdeteksi. Melanjutkan instalasi...${NC}"
echo ""

# Buat virtual environment Python
echo -e "${YELLOW}[INFO] Membuat virtual environment Python...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Gagal membuat virtual environment.${NC}"
    echo "Coba jalankan: pip install virtualenv"
    echo ""
    exit 1
fi

# Aktifkan virtual environment
echo -e "${YELLOW}[INFO] Mengaktifkan virtual environment...${NC}"
source venv/bin/activate

# Install dependencies Python
echo -e "${YELLOW}[INFO] Menginstall dependencies Python...${NC}"
pip install streamlit pandas numpy plotly python-dateutil
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Gagal menginstall dependencies Python.${NC}"
    echo ""
    exit 1
fi

# Install dependencies Node.js
echo -e "${YELLOW}[INFO] Menginstall dependencies Node.js...${NC}"
npm install cross-spawn fs-extra
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Gagal menginstall dependencies Node.js.${NC}"
    echo ""
    exit 1
fi

# Memberikan hak eksekusi pada script run.sh
chmod +x run.sh

# Verifikasi instalasi
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Instalasi Selesai!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Untuk menjalankan aplikasi:"
echo "1. Aktifkan virtual environment dengan menjalankan 'source venv/bin/activate'"
echo "2. Jalankan aplikasi dengan perintah 'node start.js'"
echo ""
echo "Atau cukup jalankan './run.sh' untuk menjalankan aplikasi secara langsung"
echo ""