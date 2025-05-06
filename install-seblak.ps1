# PowerShell Script untuk Instalasi Seblak Bujangan 
# File: install-seblak.ps1
# Jalankan dengan klik kanan -> Run with PowerShell atau buka PowerShell dan ketik: .\install-seblak.ps1

# Fungsi untuk menampilkan pesan dengan warna
function Write-ColorText {
    param (
        [string]$Text,
        [System.ConsoleColor]$Color = [System.ConsoleColor]::White
    )
    
    Write-Host $Text -ForegroundColor $Color
}

# Fungsi untuk menampilkan kotak header
function Show-Header {
    param (
        [string]$Title
    )
    
    Write-ColorText "================================================" Cyan
    Write-ColorText "  $Title" Cyan
    Write-ColorText "================================================" Cyan
    Write-Host ""
}

# Tampilkan header instalasi
Clear-Host
Show-Header "INSTALASI APLIKASI SEBLAK BUJANGAN"

Write-ColorText "✓ Menjalankan satu-klik instalasi" Yellow
Write-Host ""

# Periksa apakah script dijalankan sebagai administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-ColorText "⚠️ Script ini sebaiknya dijalankan sebagai Administrator" Yellow
    Write-ColorText "   Beberapa fungsi mungkin tidak berjalan dengan optimal" Yellow
    Write-Host ""
    $continue = Read-Host "Lanjutkan instalasi? (y/n)"
    if ($continue -ne "y") {
        Write-ColorText "Instalasi dibatalkan oleh pengguna." Red
        exit
    }
}

# 1. Periksa dan install Python jika belum ada
Write-ColorText "⚙️ Memeriksa instalasi Python..." Yellow

$pythonPath = $null
try {
    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
} catch {
    # Python not found, try python3
    try {
        $pythonPath = (Get-Command python3 -ErrorAction SilentlyContinue).Source
    } catch {
        # Neither python nor python3 found
    }
}

if ($pythonPath) {
    $pythonVersion = python --version
    Write-ColorText "✓ Python terdeteksi: $pythonVersion" Green
} else {
    Write-ColorText "❌ Python tidak terinstall." Red
    Write-Host ""
    Write-ColorText "Anda perlu menginstall Python terlebih dahulu." Yellow
    Write-ColorText "Download dari: https://www.python.org/downloads/" Cyan
    Write-ColorText "Pastikan Anda mencentang 'Add Python to PATH' saat instalasi" Yellow
    
    $installPython = Read-Host "Buka halaman download Python? (y/n)"
    if ($installPython -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }
    
    Write-ColorText "Silakan install Python terlebih dahulu, lalu jalankan script ini lagi." Yellow
    
    Write-Host ""
    Write-Host "Tekan Enter untuk keluar..."
    Read-Host
    exit
}

# 2. Periksa Node.js
Write-ColorText "⚙️ Memeriksa instalasi Node.js..." Yellow

$nodePath = $null
try {
    $nodePath = (Get-Command node -ErrorAction SilentlyContinue).Source
} catch {
    # Node.js not found
}

if ($nodePath) {
    $nodeVersion = node --version
    Write-ColorText "✓ Node.js terdeteksi: $nodeVersion" Green
} else {
    Write-ColorText "❌ Node.js tidak terinstall." Red
    Write-Host ""
    Write-ColorText "Anda perlu menginstall Node.js terlebih dahulu." Yellow
    Write-ColorText "Download dari: https://nodejs.org/en/download/" Cyan
    
    $installNode = Read-Host "Buka halaman download Node.js? (y/n)"
    if ($installNode -eq "y") {
        Start-Process "https://nodejs.org/en/download/"
    }
    
    Write-ColorText "Silakan install Node.js terlebih dahulu, lalu jalankan script ini lagi." Yellow
    
    Write-Host ""
    Write-Host "Tekan Enter untuk keluar..."
    Read-Host
    exit
}

# 3. Buat folder kosong jika belum ada
Write-ColorText "⚙️ Memeriksa struktur folder..." Yellow

$requiredFolders = @('data', 'pages', 'static', 'static/images', '.streamlit')
foreach ($folder in $requiredFolders) {
    if (-not (Test-Path -Path $folder)) {
        New-Item -Path $folder -ItemType Directory -Force | Out-Null
        Write-ColorText "✓ Folder $folder berhasil dibuat" Green
    }
}

# 4. Buat file konfigurasi Streamlit
$streamlitConfigContent = @"
[server]
headless = true
address = "0.0.0.0"
port = 5000
"@

$streamlitConfigPath = ".streamlit/config.toml"
if (-not (Test-Path -Path $streamlitConfigPath)) {
    $streamlitConfigContent | Out-File -FilePath $streamlitConfigPath -Encoding utf8
    Write-ColorText "✓ File konfigurasi Streamlit berhasil dibuat" Green
}

# 5. Buat virtual environment Python dan aktifkan
Write-ColorText "⚙️ Membuat virtual environment Python..." Yellow

$venvPath = "venv"
if (-not (Test-Path -Path $venvPath)) {
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-ColorText "⚠️ Gagal membuat virtual environment. Menginstall virtualenv..." Yellow
        python -m pip install virtualenv
        python -m virtualenv $venvPath
        
        if ($LASTEXITCODE -ne 0) {
            Write-ColorText "❌ Gagal membuat virtual environment. Lanjutkan tanpa venv." Red
        }
    } else {
        Write-ColorText "✓ Virtual environment berhasil dibuat" Green
    }
} else {
    Write-ColorText "✓ Virtual environment sudah ada" Green
}

# 6. Aktifkan virtual environment
Write-ColorText "⚙️ Mengaktifkan virtual environment..." Yellow
try {
    & "$venvPath\Scripts\Activate.ps1"
    Write-ColorText "✓ Virtual environment berhasil diaktifkan" Green
} catch {
    Write-ColorText "❌ Gagal mengaktifkan virtual environment. Instalasi akan berlanjut menggunakan Python sistem." Red
    Write-Host ""
    Write-ColorText "  Detail error: $_" Red
}

# 7. Install semua dependencies Python
Write-ColorText "⚙️ Menginstall dependencies Python..." Yellow

$pythonPackages = @(
    "streamlit",
    "pandas",
    "numpy",
    "plotly",
    "plotly-express",
    "python-dateutil",
    "matplotlib"
)

foreach ($package in $pythonPackages) {
    Write-ColorText "  Menginstall $package..." Yellow
    python -m pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-ColorText "❌ Gagal menginstall $package" Red
    } else {
        Write-ColorText "✓ Package $package berhasil diinstall" Green
    }
}

# 8. Buat file run-seblak.ps1 untuk mempermudah menjalankan aplikasi
$runScriptContent = @"
# PowerShell Script untuk Menjalankan Seblak Bujangan
# File: run-seblak.ps1
# Jalankan dengan klik kanan -> Run with PowerShell

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MENJALANKAN APLIKASI SEBLAK BUJANGAN" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Cek apakah virtual environment ada
if (Test-Path -Path "venv") {
    Write-Host "⚙️ Mengaktifkan virtual environment..." -ForegroundColor Yellow
    try {
        & ".\venv\Scripts\Activate.ps1"
        Write-Host "✓ Virtual environment berhasil diaktifkan" -ForegroundColor Green
    } catch {
        Write-Host "❌ Gagal mengaktifkan virtual environment." -ForegroundColor Red
        Write-Host "   Aplikasi akan menggunakan Python sistem." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🚀 Menjalankan aplikasi Seblak Bujangan..." -ForegroundColor Yellow
Write-Host "   Aplikasi akan terbuka di browser Anda secara otomatis" -ForegroundColor Yellow
Write-Host "   pada alamat: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️ Tekan CTRL+C untuk menghentikan aplikasi" -ForegroundColor Red
Write-Host ""

# Jalankan aplikasi Streamlit
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true

# Deaktivasi virtual environment
if (Test-Path -Path "venv") {
    deactivate
}
"@

$runScriptContent | Out-File -FilePath "run-seblak.ps1" -Encoding utf8
Write-ColorText "✓ File run-seblak.ps1 berhasil dibuat" Green

# 9. Buat file README.md dengan informasi instalasi dan penggunaan
$readmeContent = @"
# Aplikasi Seblak Bujangan

## Panduan Instalasi dan Penggunaan

### Prasyarat
Sebelum menginstall aplikasi ini, pastikan komputer Anda telah memiliki:
- Python 3.7 atau lebih baru
- Node.js

### Cara Instalasi
1. Klik kanan pada file `install-seblak.ps1`
2. Pilih "Run with PowerShell"
3. Tunggu hingga proses instalasi selesai

### Cara Menjalankan Aplikasi
1. Klik kanan pada file `run-seblak.ps1`
2. Pilih "Run with PowerShell"
3. Aplikasi akan terbuka di browser Anda pada alamat http://localhost:5000
4. Untuk menghentikan aplikasi, tekan CTRL+C di jendela PowerShell

### Informasi Tambahan
- Aplikasi ini didesain khusus untuk manajemen keuangan bisnis Seblak Bujangan
- Semua data disimpan secara lokal di folder `data`

## Fitur Utama
- Dashboard utama dengan ringkasan keuangan
- Pencatatan penjualan dan pengeluaran
- Manajemen inventaris dan stok
- Laporan keuangan dengan visualisasi grafik
"@

$readmeContent | Out-File -FilePath "README.txt" -Encoding utf8
Write-ColorText "✓ File README.txt berhasil dibuat" Green

# 10. Tampilkan informasi selesai instalasi
Write-Host ""
Show-Header "INSTALASI SELESAI!"

Write-ColorText "Aplikasi Seblak Bujangan berhasil diinstall!" Green
Write-Host ""
Write-ColorText "Untuk menjalankan aplikasi:" Yellow
Write-ColorText "1. Klik kanan pada file 'run-seblak.ps1'" White
Write-ColorText "2. Pilih 'Run with PowerShell'" White
Write-ColorText "3. Aplikasi akan terbuka di browser secara otomatis" White
Write-Host ""

$runNow = Read-Host "Jalankan aplikasi sekarang? (y/n)"
if ($runNow -eq "y") {
    Write-Host ""
    & ".\run-seblak.ps1"
} else {
    Write-Host ""
    Write-Host "Tekan Enter untuk keluar..."
    Read-Host
}