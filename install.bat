@echo off
echo ========================================
echo  Instalasi Aplikasi Seblak Bujangan
echo ========================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [31mERROR: Python tidak terinstall di sistem Anda.[0m
    echo Silakan install Python 3.7 atau yang lebih baru dari https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Cek apakah Node.js terinstall
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [31mERROR: Node.js tidak terinstall di sistem Anda.[0m
    echo Silakan install Node.js dari https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [32m[INFO] Python dan Node.js terdeteksi. Melanjutkan instalasi...[0m
echo.

REM Buat virtual environment Python
echo [33m[INFO] Membuat virtual environment Python...[0m
python -m venv venv
if %errorlevel% neq 0 (
    echo [31mERROR: Gagal membuat virtual environment.[0m
    echo Coba jalankan: pip install virtualenv
    echo.
    pause
    exit /b 1
)

REM Aktifkan virtual environment
echo [33m[INFO] Mengaktifkan virtual environment...[0m
call venv\Scripts\activate.bat

REM Install dependencies Python
echo [33m[INFO] Menginstall dependencies Python...[0m
pip install streamlit pandas numpy plotly python-dateutil
if %errorlevel% neq 0 (
    echo [31mERROR: Gagal menginstall dependencies Python.[0m
    echo.
    pause
    exit /b 1
)

REM Install dependencies Node.js
echo [33m[INFO] Menginstall dependencies Node.js...[0m
npm install cross-spawn fs-extra
if %errorlevel% neq 0 (
    echo [31mERROR: Gagal menginstall dependencies Node.js.[0m
    echo.
    pause
    exit /b 1
)

REM Verifikasi instalasi
echo.
echo [32m========================================[0m
echo [32m  Instalasi Selesai![0m
echo [32m========================================[0m
echo.
echo Untuk menjalankan aplikasi:
echo 1. Aktifkan virtual environment dengan menjalankan 'venv\Scripts\activate'
echo 2. Jalankan aplikasi dengan perintah 'node start.js'
echo.
echo Atau cukup jalankan 'run.bat' untuk menjalankan aplikasi secara langsung
echo.
pause