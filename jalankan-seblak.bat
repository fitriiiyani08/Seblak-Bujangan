@echo off
REM =============================================
REM  APLIKASI SEBLAK BUJANGAN - FILE RUNNER
REM =============================================

echo =============================================
echo  MENJALANKAN APLIKASI SEBLAK BUJANGAN
echo =============================================
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

REM Cek dan buat folder yang diperlukan
if not exist "data\" mkdir data
if not exist "pages\" mkdir pages
if not exist "static\" mkdir static
if not exist "static\images\" mkdir static\images
if not exist ".streamlit\" mkdir .streamlit

REM Buat file konfigurasi streamlit jika belum ada
if not exist ".streamlit\config.toml" (
    echo [server] > .streamlit\config.toml
    echo headless = true >> .streamlit\config.toml
    echo address = "0.0.0.0" >> .streamlit\config.toml
    echo port = 5000 >> .streamlit\config.toml
)

REM Cek apakah virtual environment ada
if exist "venv\" (
    echo [INFO] Mengaktifkan virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [INFO] Membuat virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo [WARNING] Gagal membuat virtual environment, menggunakan Python sistem.
    ) else (
        call venv\Scripts\activate.bat
    )
)

REM Install dependencies jika belum ada
pip show streamlit >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Menginstall Streamlit dan dependencies lainnya...
    pip install streamlit pandas numpy plotly plotly-express python-dateutil matplotlib
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Gagal menginstall dependencies.
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [INFO] Menjalankan aplikasi Seblak Bujangan...
echo Aplikasi akan terbuka di browser pada alamat http://localhost:5000
echo Tekan CTRL+C untuk menghentikan aplikasi
echo.

REM Jalankan aplikasi
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true

REM Deaktivasi virtual environment jika aktif
if exist "venv\" (
    call venv\Scripts\deactivate.bat
)

pause