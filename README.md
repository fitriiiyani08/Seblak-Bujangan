# Aplikasi Manajemen Keuangan Seblak Bujangan

Aplikasi manajemen keuangan khusus untuk bisnis Seblak Bujangan, dirancang dengan antarmuka berbahasa Indonesia dan tema visual cabai pedas yang unik.

## 📋 Fitur Utama

- Dashboard keuangan dengan visualisasi menarik
- Pencatatan penjualan dengan kalkulasi otomatis
- Manajemen stok bahan baku
- Pencatatan pengeluaran 
- Laporan keuangan lengkap
- Desain responsif dengan tema pedas yang menarik

## 🚀 Cara Menggunakan

### Metode 1: Menggunakan npm (Disarankan)

#### Persiapan Pertama Kali

1. Pastikan Anda sudah menginstall [Node.js](https://nodejs.org/) dan [Python](https://www.python.org/) (versi 3.7+)
2. Buka terminal/command prompt dan navigasi ke folder aplikasi
3. Jalankan setup untuk menginstall semua yang dibutuhkan:

```bash
node setup.js
```

#### Menjalankan Aplikasi

Setelah setup selesai, Anda bisa menjalankan aplikasi dengan:

```bash
npm start
```

Aplikasi akan otomatis terbuka di browser Anda dengan alamat http://localhost:5000

### Metode 2: Menggunakan Python Langsung

1. Pastikan Python 3.7+ terinstall di komputer Anda
2. Install dependencies yang diperlukan:

```bash
pip install streamlit pandas numpy plotly python-dateutil
```

3. Jalankan aplikasi:

```bash
streamlit run app.py
```

## 📊 Struktur Proyek

- `app.py`: File utama aplikasi
- `pages/`: Berisi halaman-halaman tambahan
  - `penjualan.py`: Halaman pencatatan penjualan
  - `pengeluaran.py`: Halaman pencatatan pengeluaran
  - `stok.py`: Halaman manajemen stok
  - `laporan.py`: Halaman laporan keuangan
- `data/`: Menyimpan data dalam format CSV
- `static/`: Berisi file CSS dan gambar
- `utils.py`: Berisi fungsi-fungsi pembantu

## 🌶️ Tentang Aplikasi

Aplikasi ini dirancang khusus untuk memudahkan pengelolaan keuangan usaha Seblak Bujangan dengan tampilan yang menarik dan mudah digunakan. Dengan tema merah dan elemen cabai pedas yang menjadi ciri khas, aplikasi ini tidak hanya fungsional tapi juga mencerminkan identitas produk Seblak yang pedas dan menggugah selera.