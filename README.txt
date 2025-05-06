# Aplikasi Seblak Bujangan

## Panduan Instalasi dan Penggunaan Windows (Cara Termudah)

### Prasyarat
Sebelum menginstall aplikasi ini, pastikan komputer Anda telah memiliki:
- Python 3.7 atau lebih baru (Download: https://www.python.org/downloads/)
  Pastikan centang opsi "Add Python to PATH" saat instalasi

### Cara Instalasi Sangat Mudah (Klik 2x pada file batch)
1. Double-click pada file `install-seblak.bat`
2. Tunggu hingga proses instalasi selesai
3. Ketik "y" jika ditanya apakah ingin menjalankan aplikasi sekarang

### Cara Menjalankan Aplikasi (Sangat Mudah)
1. Double-click pada file `jalankan-seblak.bat`
2. Aplikasi akan terbuka di browser Anda pada alamat http://localhost:5000
3. Untuk menghentikan aplikasi, tekan CTRL+C di jendela command prompt

### Instalasi Alternatif dengan PowerShell (Jika Dibutuhkan)
Jika Anda lebih suka menggunakan PowerShell:
1. Klik kanan file `install-seblak.ps1`, pilih "Run with PowerShell"
2. Jika muncul error tentang kebijakan keamanan, jalankan PowerShell sebagai Administrator dan ketik:
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