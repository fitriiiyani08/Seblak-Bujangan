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