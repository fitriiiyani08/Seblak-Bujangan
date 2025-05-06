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
const requiredDirs = ['pages', 'static'];
requiredDirs.forEach(dir => {
  if (!fs.existsSync(path.join(__dirname, dir))) {
    fs.mkdirSync(path.join(__dirname, dir));
    console.log(`✅ Folder ${dir} berhasil dibuat`);
  }
});

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