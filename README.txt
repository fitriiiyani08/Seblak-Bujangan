# Aplikasi Seblak Bujangan

## Panduan Instalasi dan Penggunaan Windows

### Prasyarat
Sebelum menginstall aplikasi ini, pastikan komputer Anda telah memiliki:
- Python 3.7 atau lebih baru (Download: https://www.python.org/downloads/)
- Node.js (Download: https://nodejs.org/)

### Cara Instalasi (Opsi Mudah)
1. Klik kanan pada file `install-seblak.ps1`
2. Pilih "Run with PowerShell"
3. Tunggu hingga proses instalasi selesai
4. Jika muncul pesan tentang policy, ketik "Y" lalu Enter

### Cara Menjalankan Aplikasi (Opsi Mudah)
1. Klik kanan pada file `run-seblak.ps1`
2. Pilih "Run with PowerShell"
3. Aplikasi akan terbuka di browser Anda pada alamat http://localhost:5000
4. Untuk menghentikan aplikasi, tekan CTRL+C di jendela PowerShell

### Jika Ada Masalah Dengan PowerShell
Jika PowerShell tidak bisa menjalankan script karena kebijakan keamanan, buka PowerShell sebagai Administrator dan jalankan:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Backup Data
Semua data aplikasi disimpan di folder `data`. Untuk backup, cukup salin folder tersebut.

### Fitur Utama
- Dashboard utama dengan ringkasan keuangan
- Pencatatan penjualan dan pengeluaran
- Manajemen inventaris dan stok bahan
- Laporan keuangan dengan visualisasi grafik
- Analisis laba/rugi

### Struktur Folder
- `data/`: Menyimpan semua file data (CSV)
- `pages/`: Halaman-halaman aplikasi
- `static/`: File statis (CSS, gambar)

### Cara Uninstall
Aplikasi ini tidak mengubah registry Windows. Untuk uninstall, cukup hapus folder aplikasi.