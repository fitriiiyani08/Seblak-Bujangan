/**
 * Starter script untuk aplikasi Seblak Bujangan
 * Script ini memungkinkan penggunaan npm start untuk menjalankan aplikasi Streamlit
 */

const spawn = require('cross-spawn');
const fs = require('fs-extra');
const path = require('path');

// Cek apakah directory data ada, jika tidak buat directory tersebut
if (!fs.existsSync(path.join(__dirname, 'data'))) {
  fs.mkdirSync(path.join(__dirname, 'data'));
  console.log('✅ Folder data berhasil dibuat');
}

// Cek apakah structure direktori lainnya ada
const requiredDirs = ['pages', 'static', 'static/images'];
requiredDirs.forEach(dir => {
  if (!fs.existsSync(path.join(__dirname, dir))) {
    fs.mkdirSync(path.join(__dirname, dir), { recursive: true });
    console.log(`✅ Folder ${dir} berhasil dibuat`);
  }
});

// Cek file data pesanan
const pesananPath = path.join(__dirname, 'data', 'pesanan.csv');
if (!fs.existsSync(pesananPath)) {
  console.log('📝 Membuat file data/pesanan.csv...');
  const pesananHeader = 'id,tanggal,nama_pembeli,produk,jumlah,harga_total,tingkat_kepedasan,catatan,metode_pembayaran,status_pesanan,tipe_pesanan,waktu_pemesanan,waktu_selesai';
  fs.writeFileSync(pesananPath, pesananHeader);
}

// Cek file data produk
const produkPath = path.join(__dirname, 'data', 'produk.csv');
if (!fs.existsSync(produkPath)) {
  console.log('📝 Membuat file data/produk.csv...');
  const produkData = `nama,harga,deskripsi
Seblak Original,15000,Seblak Original dengan kerupuk dan telur
Seblak Seafood,20000,Seblak dengan tambahan seafood (cumi udang dsb)
Seblak Komplit,25000,Seblak dengan semua topping
Seblak Mie,18000,Seblak dengan tambahan mie
Seblak Ayam,17000,Seblak dengan tambahan potongan ayam
Seblak Tulang,16000,Seblak dengan tambahan tulang rawan
Seblak Baso,16500,Seblak dengan tambahan baso sapi
Seblak Ceker,15500,Seblak dengan tambahan ceker ayam`;
  fs.writeFileSync(produkPath, produkData);
}

console.log('🚀 Menjalankan aplikasi Seblak Bujangan...');
console.log('⏳ Mohon tunggu sebentar, aplikasi sedang dimuat...');

// Jalankan aplikasi Streamlit
const streamlit = spawn('streamlit', ['run', 'app.py', '--server.port', '5000'], {
  stdio: 'inherit',
  shell: true
});

// Handle proses exit
streamlit.on('close', (code) => {
  if (code !== 0) {
    console.log(`❌ Aplikasi berhenti dengan kode exit: ${code}`);
    console.log('💡 Pastikan Streamlit terinstall dengan menjalankan: pip install streamlit pandas numpy plotly python-dateutil');
  }
  process.exit(code);
});

// Handle error
streamlit.on('error', (err) => {
  console.error(`❌ Error saat menjalankan aplikasi: ${err.message}`);
  console.log('💡 Pastikan Python dan Streamlit terinstall di sistem Anda');
  process.exit(1);
});

// Log pesan untuk CTRL+C
console.log('ℹ️  Tekan CTRL+C untuk keluar dari aplikasi');