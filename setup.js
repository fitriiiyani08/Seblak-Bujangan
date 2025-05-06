/**
 * Setup script untuk aplikasi Seblak Bujangan
 * Script ini membantu menyiapkan lingkungan dan instalasi dependencies
 */

const spawn = require('cross-spawn');
const fs = require('fs-extra');
const path = require('path');

console.log('🔧 Memulai setup aplikasi Seblak Bujangan...');

// Fungsi untuk menjalankan perintah shell
function runCommand(command, args) {
  return new Promise((resolve, reject) => {
    console.log(`🔄 Menjalankan: ${command} ${args.join(' ')}`);
    
    const childProcess = spawn(command, args, {
      stdio: 'inherit',
      shell: true
    });
    
    childProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Command ${command} failed with code ${code}`));
        return;
      }
      resolve();
    });
    
    childProcess.on('error', (err) => {
      reject(err);
    });
  });
}

// Membuat struktur folder
async function createFolderStructure() {
  console.log('📁 Membuat struktur folder...');
  
  const folders = ['data', 'pages', 'static', 'static/images'];
  
  folders.forEach(folder => {
    const folderPath = path.join(__dirname, folder);
    if (!fs.existsSync(folderPath)) {
      fs.mkdirSync(folderPath, { recursive: true });
      console.log(`✅ Folder ${folder} berhasil dibuat`);
    } else {
      console.log(`ℹ️  Folder ${folder} sudah ada`);
    }
  });
}

// Install dependencies Python
async function installDependencies() {
  console.log('📦 Menginstall dependencies Python...');
  
  try {
    await runCommand('pip', ['install', 'streamlit', 'pandas', 'numpy', 'plotly', 'python-dateutil']);
    console.log('✅ Dependencies Python berhasil diinstall');
  } catch (error) {
    console.error('❌ Gagal menginstall dependencies Python:', error.message);
    console.log('💡 Coba jalankan manual: pip install streamlit pandas numpy plotly python-dateutil');
  }
}

// Jalankan semua fungsi setup
async function setup() {
  try {
    await createFolderStructure();
    await installDependencies();
    
    console.log('\n✅ Setup berhasil!');
    console.log('🚀 Untuk menjalankan aplikasi, gunakan perintah: npm start');
  } catch (error) {
    console.error('\n❌ Setup gagal:', error.message);
  }
}

// Jalankan setup
setup();