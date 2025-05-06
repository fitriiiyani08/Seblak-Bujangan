@echo off
REM =============================================
REM  APLIKASI SEBLAK BUJANGAN - INSTALLER
REM =============================================

title Instalasi Seblak Bujangan

echo =============================================
echo  INSTALASI APLIKASI SEBLAK BUJANGAN
echo =============================================
echo.

REM Cek ketersediaan Python
echo [PROSES] Memeriksa instalasi Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python tidak terdeteksi di sistem Anda.
    echo Silakan install Python 3.7 atau lebih baru dari https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo [OK] Python terdeteksi.
)

echo.
echo [PROSES] Membuat struktur folder...
REM Buat folder yang diperlukan
if not exist "data\" (
    mkdir data
    echo [OK] Folder data berhasil dibuat.
) else (
    echo [OK] Folder data sudah ada.
)

if not exist "pages\" (
    mkdir pages
    echo [OK] Folder pages berhasil dibuat.
) else (
    echo [OK] Folder pages sudah ada.
)

if not exist "static\" (
    mkdir static
    echo [OK] Folder static berhasil dibuat.
) else (
    echo [OK] Folder static sudah ada.
)

if not exist "static\images\" (
    mkdir static\images
    echo [OK] Folder static\images berhasil dibuat.
) else (
    echo [OK] Folder static\images sudah ada.
)

if not exist ".streamlit\" (
    mkdir .streamlit
    echo [OK] Folder .streamlit berhasil dibuat.
) else (
    echo [OK] Folder .streamlit sudah ada.
)

echo.
echo [PROSES] Membuat file konfigurasi Streamlit...
REM Buat file konfigurasi streamlit
echo [server] > .streamlit\config.toml
echo headless = true >> .streamlit\config.toml
echo address = "0.0.0.0" >> .streamlit\config.toml
echo port = 5000 >> .streamlit\config.toml
echo [OK] File konfigurasi Streamlit berhasil dibuat.

echo.
echo [PROSES] Membuat virtual environment Python...
REM Buat virtual environment jika belum ada
if exist "venv\" (
    echo [OK] Virtual environment sudah ada.
) else (
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] Gagal membuat virtual environment dengan venv.
        echo [PROSES] Mencoba dengan virtualenv...
        
        pip install virtualenv
        python -m virtualenv venv
        
        if %ERRORLEVEL% NEQ 0 (
            echo [WARNING] Gagal membuat virtual environment dengan virtualenv.
            echo [INFO] Instalasi akan menggunakan Python sistem.
        ) else (
            echo [OK] Virtual environment berhasil dibuat dengan virtualenv.
        )
    ) else (
        echo [OK] Virtual environment berhasil dibuat dengan venv.
    )
)

echo.
echo [PROSES] Mengaktifkan virtual environment...
REM Aktifkan virtual environment
if exist "venv\" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment berhasil diaktifkan.
) else (
    echo [WARNING] Menggunakan Python sistem.
)

echo.
echo [PROSES] Menginstall dependencies Python...
REM Install semua dependencies
pip install streamlit pandas numpy plotly plotly-express python-dateutil matplotlib
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal menginstall dependencies Python.
    echo.
    pause
    exit /b 1
) else (
    echo [OK] Dependencies Python berhasil diinstall.
)

echo.
echo =============================================
echo  INSTALASI SELESAI
echo =============================================
echo.
echo Aplikasi Seblak Bujangan berhasil diinstall!
echo.
echo Untuk menjalankan aplikasi, double-click pada file:
echo   jalankan-seblak.bat
echo.

REM Deaktivasi virtual environment jika aktif
if exist "venv\" (
    call venv\Scripts\deactivate.bat
)

set /P run_now=Jalankan aplikasi sekarang? (y/n): 
if /I "%run_now%"=="y" (
    start jalankan-seblak.bat
) else (
    pause
)