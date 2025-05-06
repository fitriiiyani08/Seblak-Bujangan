# Panduan Instalasi Aplikasi Seblak Bujangan

Dokumen ini berisi panduan langkah demi langkah untuk menginstall dan menjalankan aplikasi manajemen keuangan Seblak Bujangan di laptop Anda.

## Persyaratan Sistem

Sebelum memulai, pastikan sistem Anda memiliki komponen berikut:

1. **Python 3.7 atau lebih baru**
   - Download dari: [python.org](https://www.python.org/downloads/)
   - Pastikan Anda mencentang "Add Python to PATH" saat instalasi

2. **Node.js**
   - Download dari: [nodejs.org](https://nodejs.org/)
   - Pilih versi LTS (Long Term Support) untuk stabilitas

## Cara Instalasi (Windows PowerShell)

### Metode 1: Menggunakan PowerShell Script (Direkomendasikan)

1. **Extract file zip** ke folder pilihan Anda
2. **Buka PowerShell** dengan hak administrator:
   - Klik kanan pada menu Start > Windows PowerShell
   - Pilih "Run as Administrator"
3. **Navigasi ke folder** tempat Anda mengekstrak file:
   ```
   cd "C:\Path\To\Seblak-Bujangan"
   ```
4. **Izinkan eksekusi script**:
   ```
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
5. **Jalankan script setup**:
   ```
   .\easy-setup.ps1
   ```
6. **Tunggu proses instalasi selesai**. Script akan:
   - Membuat virtual environment Python
   - Menginstall semua package yang dibutuhkan
   - Mengatur konfigurasi npm untuk aplikasi

### Metode 2: Menggunakan npm

1. **Extract file zip** ke folder pilihan Anda
2. **Buka PowerShell** atau Command Prompt
3. **Navigasi ke folder** tempat Anda mengekstrak file:
   ```
   cd "C:\Path\To\Seblak-Bujangan"
   ```
4. **Install dependencies Node.js**:
   ```
   npm install
   ```
5. **Buat virtual environment Python**:
   ```
   python -m venv venv
   ```
6. **Aktifkan virtual environment**:
   - Di PowerShell: `.\venv\Scripts\Activate.ps1`
   - Di Command Prompt: `venv\Scripts\activate.bat`
7. **Install Python packages**:
   ```
   pip install streamlit pandas numpy plotly python-dateutil
   ```

## Cara Menjalankan Aplikasi

### Metode 1: Menggunakan Script PowerShell (Direkomendasikan)

Setelah instalasi selesai:
1. **Buka PowerShell**
2. **Navigasi ke folder aplikasi**
3. **Jalankan script**:
   ```
   .\run-app.ps1
   ```

### Metode 2: Menggunakan npm start

1. **Aktifkan virtual environment terlebih dahulu**:
   - Di PowerShell: `.\venv\Scripts\Activate.ps1`
   - Di Command Prompt: `venv\Scripts\activate.bat`
2. **Jalankan aplikasi**:
   ```
   npm start
   ```

Aplikasi akan terbuka secara otomatis di browser dengan alamat [http://localhost:5000](http://localhost:5000)

## Mengatasi Masalah Umum

### Script tidak bisa dijalankan

Jika Anda mendapatkan error tentang eksekusi script yang dilarang, jalankan PowerShell sebagai Administrator dan ketik:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Package atau modul tidak ditemukan

Pastikan virtual environment sudah aktif (Anda akan melihat `(venv)` di awal baris PowerShell). Jika belum aktif, jalankan:

```
.\venv\Scripts\Activate.ps1
```

### Port 5000 sudah digunakan

Jika port 5000 sudah digunakan oleh aplikasi lain, edit file `start.js` dan ubah angka 5000 ke port lain yang tersedia (misalnya 8000, 8080).