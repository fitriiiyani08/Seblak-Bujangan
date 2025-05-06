/**
 * Starter script untuk aplikasi Seblak Bujangan
 * Script ini memungkinkan penggunaan npm start untuk menjalankan aplikasi Streamlit
 */

const spawn = require('cross-spawn');
const fs = require('fs-extra');
const path = require('path');

// Port untuk menjalankan aplikasi
const PORT = 5000;

console.log('🚀 Menjalankan aplikasi Seblak Bujangan...');

// Pastikan folder .streamlit ada
const streamlitConfigDir = path.join(__dirname, '.streamlit');
if (!fs.existsSync(streamlitConfigDir)) {
  fs.mkdirSync(streamlitConfigDir, { recursive: true });
  console.log('✅ Folder .streamlit berhasil dibuat');
}

// Buat atau perbarui file konfigurasi Streamlit
const configPath = path.join(streamlitConfigDir, 'config.toml');
const configContent = `
[server]
headless = true
address = "0.0.0.0"
port = ${PORT}
`;

if (!fs.existsSync(configPath) || fs.readFileSync(configPath, 'utf8') !== configContent) {
  fs.writeFileSync(configPath, configContent);
  console.log('✅ File konfigurasi Streamlit berhasil dibuat/diperbarui');
}

// Pastikan semua folder yang diperlukan sudah ada
const requiredFolders = ['data', 'pages', 'static', 'static/images'];
requiredFolders.forEach(folder => {
  const folderPath = path.join(__dirname, folder);
  if (!fs.existsSync(folderPath)) {
    fs.mkdirSync(folderPath, { recursive: true });
    console.log(`✅ Folder ${folder} berhasil dibuat`);
  }
});

try {
  // Jalankan aplikasi Streamlit
  console.log(`🔥 Menjalankan server pada http://localhost:${PORT}`);
  console.log('📊 Aplikasi akan terbuka di browser secara otomatis.');
  console.log('🛑 Tekan Ctrl+C untuk menghentikan server.');
  
  // Deteksi OS untuk menentukan command yang tepat
  const isWindows = process.platform === 'win32';
  
  let streamlitProcess;
  
  if (isWindows) {
    // Windows - coba gunakan streamlit dari virtual environment
    if (fs.existsSync(path.join(__dirname, 'venv', 'Scripts', 'streamlit.exe'))) {
      streamlitProcess = spawn(
        path.join(__dirname, 'venv', 'Scripts', 'streamlit.exe'),
        ['run', 'app.py', '--server.port', PORT.toString()],
        { stdio: 'inherit' }
      );
    } else {
      // Gunakan streamlit global jika tidak ada di venv
      streamlitProcess = spawn(
        'streamlit',
        ['run', 'app.py', '--server.port', PORT.toString()],
        { stdio: 'inherit' }
      );
    }
  } else {
    // MacOS/Linux - coba gunakan streamlit dari virtual environment
    if (fs.existsSync(path.join(__dirname, 'venv', 'bin', 'streamlit'))) {
      streamlitProcess = spawn(
        path.join(__dirname, 'venv', 'bin', 'streamlit'),
        ['run', 'app.py', '--server.port', PORT.toString()],
        { stdio: 'inherit' }
      );
    } else {
      // Gunakan streamlit global jika tidak ada di venv
      streamlitProcess = spawn(
        'streamlit',
        ['run', 'app.py', '--server.port', PORT.toString()],
        { stdio: 'inherit' }
      );
    }
  }
  
  // Handle event ketika streamlit berakhir
  streamlitProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`❌ Streamlit keluar dengan kode: ${code}`);
    }
    console.log('👋 Terima kasih telah menggunakan aplikasi Seblak Bujangan');
  });
} catch (error) {
  console.error('❌ Gagal menjalankan Streamlit:', error.message);
  console.error('📝 Pastikan Python dan Streamlit sudah terinstall dengan benar');
  process.exit(1);
}