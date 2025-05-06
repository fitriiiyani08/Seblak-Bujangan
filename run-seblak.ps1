# PowerShell Script untuk Menjalankan Seblak Bujangan
# File: run-seblak.ps1
# Jalankan dengan klik kanan -> Run with PowerShell

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

# Tampilkan header
Clear-Host
Show-Header "MENJALANKAN APLIKASI SEBLAK BUJANGAN"

# Cek apakah virtual environment ada
if (Test-Path -Path "venv") {
    Write-ColorText "⚙️ Mengaktifkan virtual environment..." Yellow
    try {
        & ".\venv\Scripts\Activate.ps1"
        Write-ColorText "✓ Virtual environment berhasil diaktifkan" Green
    } catch {
        Write-ColorText "❌ Gagal mengaktifkan virtual environment." Red
        Write-ColorText "   Aplikasi akan menggunakan Python sistem." Yellow
        
        # Cek apakah Python dan Streamlit terinstall di sistem
        $streamlitInstalled = $false
        try {
            $streamlitVersion = streamlit --version
            $streamlitInstalled = $true
        } catch {
            $streamlitInstalled = $false
        }
        
        if (-not $streamlitInstalled) {
            Write-ColorText "❌ Streamlit tidak terinstall di sistem." Red
            Write-ColorText "   Menginstall Streamlit dan dependencies lainnya..." Yellow
            
            python -m pip install streamlit pandas numpy plotly plotly-express python-dateutil matplotlib
            
            if ($LASTEXITCODE -ne 0) {
                Write-ColorText "❌ Gagal menginstall dependencies." Red
                Write-ColorText "   Silakan jalankan install-seblak.ps1 untuk memperbaiki masalah." Yellow
                Write-Host ""
                Write-Host "Tekan Enter untuk keluar..."
                Read-Host
                exit
            }
        }
    }
}

Write-Host ""
Write-ColorText "🚀 Menjalankan aplikasi Seblak Bujangan..." Yellow
Write-ColorText "   Aplikasi akan terbuka di browser Anda secara otomatis" Yellow
Write-ColorText "   pada alamat: http://localhost:5000" Cyan
Write-Host ""
Write-ColorText "⚠️ Tekan CTRL+C untuk menghentikan aplikasi" Red
Write-Host ""

# Jalankan aplikasi Streamlit
try {
    # Pastikan folder data sudah ada
    $requiredFolders = @('data', 'pages', 'static', 'static/images', '.streamlit')
    foreach ($folder in $requiredFolders) {
        if (-not (Test-Path -Path $folder)) {
            New-Item -Path $folder -ItemType Directory -Force | Out-Null
        }
    }
    
    # Pastikan file config.toml sudah ada
    $streamlitConfigPath = ".streamlit/config.toml"
    if (-not (Test-Path -Path $streamlitConfigPath)) {
        $streamlitConfigContent = @"
[server]
headless = true
address = "0.0.0.0"
port = 5000
"@
        $streamlitConfigContent | Out-File -FilePath $streamlitConfigPath -Encoding utf8
    }
    
    # Jalankan aplikasi
    streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
} catch {
    Write-ColorText "❌ Gagal menjalankan aplikasi." Red
    Write-ColorText "   Detail error: $_" Red
    Write-ColorText "   Silakan jalankan install-seblak.ps1 untuk memperbaiki masalah." Yellow
}

# Deaktivasi virtual environment
if (Test-Path -Path "venv") {
    try {
        deactivate
    } catch {
        # Deactivate failed, but we can ignore this
    }
}