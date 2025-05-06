@echo off
REM Batch file untuk menjalankan aplikasi Seblak Bujangan pada Windows
TITLE Aplikasi Seblak Bujangan

echo ========================================
echo   Menjalankan Aplikasi Seblak Bujangan
echo ========================================
echo.

REM Cek jika virtual environment ada
if not exist venv (
    echo [ERROR] Virtual environment tidak ditemukan.
    echo Jalankan install.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

REM Aktifkan virtual environment
echo [PROSES] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Jalankan aplikasi menggunakan npm start
echo [PROSES] Menjalankan aplikasi Seblak Bujangan...
echo Aplikasi akan terbuka di browser secara otomatis pada http://localhost:5000
echo Tekan Ctrl+C untuk menghentikan aplikasi.
echo.

node start.js

REM Deaktivasi virtual environment
call venv\Scripts\deactivate.bat

pause