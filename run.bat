@echo off
echo ========================================
echo  Menjalankan Aplikasi Seblak Bujangan
echo ========================================
echo.

REM Cek apakah folder venv ada
if not exist venv (
    echo [31mVirtual environment tidak ditemukan.[0m
    echo Jalankan install.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

REM Aktifkan virtual environment
echo [33m[INFO] Mengaktifkan virtual environment...[0m
call venv\Scripts\activate.bat

REM Jalankan aplikasi
echo [33m[INFO] Menjalankan aplikasi Seblak Bujangan...[0m
echo [33m[INFO] Aplikasi akan terbuka di browser secara otomatis.[0m
echo [33m[INFO] Tekan Ctrl+C untuk menghentikan aplikasi.[0m
echo.

node start.js

REM Deaktivasi virtual environment saat selesai
call venv\Scripts\deactivate.bat