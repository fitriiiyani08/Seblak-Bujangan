@echo off
REM Batch file untuk instalasi aplikasi Seblak Bujangan pada Windows
TITLE Instalasi Seblak Bujangan

echo ========================================
echo   Instalasi Aplikasi Seblak Bujangan
echo ========================================
echo.

REM Cek ketersediaan Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak terdeteksi di sistem Anda.
    echo Silakan install Python 3.7 atau lebih baru dari https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Cek ketersediaan Node.js
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js tidak terdeteksi di sistem Anda.
    echo Silakan install Node.js dari https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python dan Node.js terdeteksi. Melanjutkan instalasi...
echo.

REM Membuat virtual environment
echo [PROSES] Membuat virtual environment Python...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal membuat virtual environment.
    echo Coba install virtualenv terlebih dahulu dengan: pip install virtualenv
    echo.
    pause
    exit /b 1
)

REM Aktifkan virtual environment
echo [PROSES] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies Python
echo [PROSES] Menginstall dependencies Python...
pip install streamlit pandas numpy plotly plotly-express python-dateutil matplotlib
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal menginstall dependencies Python.
    echo.
    pause
    exit /b 1
)

REM Install dependencies Node.js
echo [PROSES] Menginstall dependencies Node.js...
npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal menginstall dependencies Node.js.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Instalasi Selesai!
echo ========================================
echo.
echo Untuk menjalankan aplikasi:
echo 1. Buka Command Prompt di folder ini
echo 2. Jalankan perintah: run.bat
echo.
echo Atau, cukup klik file run.bat secara langsung!
echo.

pause