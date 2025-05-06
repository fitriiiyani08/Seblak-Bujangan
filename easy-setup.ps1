# PowerShell script untuk setup aplikasi Seblak Bujangan
# Jalankan script ini di PowerShell dengan mengetikkan:
# .\easy-setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Aplikasi Seblak Bujangan" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Fungsi untuk memeriksa apakah sebuah program terinstall
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if (Get-Command $command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Cek apakah Python terinstall
if (-not (Test-CommandExists python)) {
    Write-Host "Python tidak terinstall di sistem Anda." -ForegroundColor Red
    Write-Host "Silakan install Python 3.7 atau yang lebih baru dari https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Cek apakah Node.js terinstall
if (-not (Test-CommandExists node)) {
    Write-Host "Node.js tidak terinstall di sistem Anda." -ForegroundColor Red
    Write-Host "Silakan install Node.js dari https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "Python dan Node.js terdeteksi. Melanjutkan setup..." -ForegroundColor Green
Write-Host ""

# Buat virtual environment Python
Write-Host "Membuat virtual environment Python..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "Gagal membuat virtual environment. Coba install virtualenv terlebih dahulu dengan:" -ForegroundColor Red
    Write-Host "pip install virtualenv" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Aktifkan virtual environment
Write-Host "Mengaktifkan virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies Python
Write-Host "Menginstall dependencies Python..." -ForegroundColor Yellow
pip install streamlit pandas numpy plotly plotly-express python-dateutil matplotlib
if ($LASTEXITCODE -ne 0) {
    Write-Host "Gagal menginstall dependencies Python." -ForegroundColor Red
    Write-Host ""
    exit 1
}

# Install dependencies Node.js
Write-Host "Menginstall dependencies Node.js..." -ForegroundColor Yellow
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Gagal menginstall dependencies Node.js." -ForegroundColor Red
    Write-Host ""
    exit 1
}

# Verifikasi instalasi
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Instalasi Selesai!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Cara menjalankan aplikasi:" -ForegroundColor Yellow
Write-Host "1. Buka PowerShell dan navigasi ke folder aplikasi"
Write-Host "2. Aktifkan virtual environment dengan: .\venv\Scripts\Activate.ps1"
Write-Host "3. Jalankan aplikasi dengan: npm start"
Write-Host ""
Write-Host "Atau, gunakan script powershell berikut untuk langsung menjalankan:" -ForegroundColor Yellow
Write-Host ".\run-app.ps1"
Write-Host ""

# Buat file run-app.ps1 untuk mempermudah menjalankan aplikasi
$runAppContent = @"
# PowerShell script untuk menjalankan aplikasi Seblak Bujangan
# Jalankan dengan: .\run-app.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Menjalankan Aplikasi Seblak Bujangan" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cek apakah folder venv ada
if (-not (Test-Path -Path "venv" -PathType Container)) {
    Write-Host "Virtual environment tidak ditemukan." -ForegroundColor Red
    Write-Host "Jalankan easy-setup.ps1 terlebih dahulu." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Aktifkan virtual environment
Write-Host "Mengaktifkan virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Jalankan aplikasi
Write-Host "Menjalankan aplikasi Seblak Bujangan..." -ForegroundColor Yellow
Write-Host "Aplikasi akan terbuka di browser secara otomatis." -ForegroundColor Yellow
Write-Host "Tekan Ctrl+C untuk menghentikan aplikasi." -ForegroundColor Yellow
Write-Host ""

node start.js

# Deaktivasi virtual environment saat selesai
deactivate
"@

# Simpan ke file
$runAppContent | Out-File -FilePath "run-app.ps1" -Encoding utf8
Write-Host "File run-app.ps1 berhasil dibuat." -ForegroundColor Green

Write-Host "Tekan tombol apa saja untuk keluar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")