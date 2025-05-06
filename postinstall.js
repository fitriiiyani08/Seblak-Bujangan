/**
 * Script postinstall untuk aplikasi Seblak Bujangan
 * Berjalan otomatis setelah npm install selesai
 */

const fs = require('fs-extra');
const path = require('path');
const { spawn } = require('cross-spawn');

console.log('📋 Menjalankan setup pasca instalasi...');

// Periksa dan buat struktur folder jika belum ada
const folders = ['data', 'pages', 'static', 'static/images'];
folders.forEach(folder => {
  const folderPath = path.join(__dirname, folder);
  if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
    console.log(`✅ Folder ${folder} berhasil dibuat`);
  }
});

// Tambahkan skrip npm ke package.json jika belum ada
try {
  const packageJsonPath = path.join(__dirname, 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = require(packageJsonPath);
    
    // Tambahkan script jika belum ada
    packageJson.scripts = packageJson.scripts || {};
    
    if (!packageJson.scripts.setup) {
      packageJson.scripts.setup = 'node setup.js';
      console.log('✅ Menambahkan script setup ke package.json');
    }
    
    if (!packageJson.scripts.start) {
      packageJson.scripts.start = 'node start.js';
      console.log('✅ Menambahkan script start ke package.json');
    }
    
    // Tambahkan informasi tentang aplikasi
    if (packageJson.name === 'workspace') {
      packageJson.name = 'seblak-bujangan';
      console.log('✅ Memperbarui nama paket menjadi seblak-bujangan');
    }
    
    if (!packageJson.description || packageJson.description === '') {
      packageJson.description = 'Aplikasi Manajemen Keuangan Seblak Bujangan';
      console.log('✅ Menambahkan deskripsi paket');
    }
    
    // Simpan perubahan
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
  }
} catch (error) {
  console.error('❌ Gagal memperbarui package.json:', error.message);
}

console.log('\n✅ Setup pasca instalasi selesai');
console.log('📝 Untuk menjalankan aplikasi:');
console.log('  1. npm run setup   - untuk menyiapkan semua dependencies');
console.log('  2. npm start       - untuk menjalankan aplikasi Seblak Bujangan');