"""
Modul untuk sinkronisasi data antara pesanan, penjualan, dan laporan
Digunakan untuk memastikan data konsisten di seluruh aplikasi
"""

import pandas as pd
import os
from datetime import datetime
from utils import load_data, save_data

def sync_pesanan_to_penjualan():
    """
    Menyinkronkan data dari pesanan yang selesai ke data penjualan
    Hanya pesanan dengan status "Selesai" yang akan ditambahkan ke penjualan
    """
    # Load data
    pesanan_file = "data/pesanan.csv"
    keuangan_file = "data/keuangan.csv"
    
    if not os.path.exists(pesanan_file):
        print("File pesanan tidak ditemukan")
        return False
    
    try:
        pesanan_df = pd.read_csv(pesanan_file)
    except Exception as e:
        print(f"Error saat membaca file pesanan: {e}")
        return False
    
    # Buat file keuangan.csv jika belum ada
    if not os.path.exists(keuangan_file):
        keuangan_df = pd.DataFrame(columns=['tanggal', 'jenis', 'kategori', 'deskripsi', 'jumlah'])
        keuangan_df.to_csv(keuangan_file, index=False)
    
    try:
        keuangan_df = pd.read_csv(keuangan_file)
    except Exception as e:
        print(f"Error saat membaca file keuangan: {e}")
        keuangan_df = pd.DataFrame(columns=['tanggal', 'jenis', 'kategori', 'deskripsi', 'jumlah'])
    
    # Filter pesanan yang selesai dan belum disinkronkan
    if 'disinkronkan' not in pesanan_df.columns:
        pesanan_df['disinkronkan'] = False
    
    # Pastikan tipe data disinkronkan adalah boolean
    pesanan_df['disinkronkan'] = pesanan_df['disinkronkan'].astype(bool)
    
    # Filter pesanan yang selesai dan belum disinkronkan
    pesanan_selesai = pesanan_df[(pesanan_df['status_pesanan'] == 'Selesai') & 
                                (pesanan_df['disinkronkan'] == False)]
    
    # Jika tidak ada pesanan selesai yang belum disinkronkan, keluar
    if pesanan_selesai.empty:
        print("Tidak ada pesanan baru yang perlu disinkronkan")
        return True
    
    # Konversi pesanan ke format data keuangan
    new_entries = []
    for _, pesanan in pesanan_selesai.iterrows():
        # Siapkan entri baru untuk keuangan.csv
        new_entry = {
            'tanggal': pesanan['tanggal'],
            'jenis': 'Pendapatan',
            'kategori': 'Penjualan',
            'deskripsi': f"{pesanan['produk']} ({pesanan['jumlah']} porsi)",
            'jumlah': pesanan['harga_total']
        }
        new_entries.append(new_entry)
        
        # Tandai pesanan sebagai sudah disinkronkan
        pesanan_df.loc[pesanan_df['id'] == pesanan['id'], 'disinkronkan'] = True
    
    # Tambahkan entri baru ke keuangan_df
    new_entries_df = pd.DataFrame(new_entries)
    keuangan_df = pd.concat([keuangan_df, new_entries_df], ignore_index=True)
    
    # Simpan perubahan
    keuangan_df.to_csv(keuangan_file, index=False)
    pesanan_df.to_csv(pesanan_file, index=False)
    
    print(f"Berhasil menyinkronkan {len(new_entries)} pesanan ke data penjualan")
    return True

def check_pending_sync():
    """
    Memeriksa apakah ada pesanan yang menunggu sinkronisasi
    """
    # Load data
    pesanan_file = "data/pesanan.csv"
    
    if not os.path.exists(pesanan_file):
        return 0
    
    try:
        pesanan_df = pd.read_csv(pesanan_file)
    except Exception:
        return 0
    
    # Tambahkan kolom disinkronkan jika belum ada
    if 'disinkronkan' not in pesanan_df.columns:
        pesanan_df['disinkronkan'] = False
        pesanan_df.to_csv(pesanan_file, index=False)
    
    # Pastikan tipe data disinkronkan adalah boolean
    pesanan_df['disinkronkan'] = pesanan_df['disinkronkan'].astype(bool)
    
    # Hitung pesanan yang perlu disinkronkan
    pesanan_pending = pesanan_df[(pesanan_df['status_pesanan'] == 'Selesai') & 
                                (pesanan_df['disinkronkan'] == False)]
    
    return len(pesanan_pending)

def run_auto_sync():
    """
    Menjalankan sinkronisasi otomatis saat aplikasi dimulai
    """
    pending_count = check_pending_sync()
    if pending_count > 0:
        print(f"Menemukan {pending_count} pesanan yang belum disinkronkan")
        sync_pesanan_to_penjualan()
        return True
    return False

# Fungsi untuk sinkronisasi manual
def manual_sync():
    """
    Menjalankan sinkronisasi manual
    """
    result = sync_pesanan_to_penjualan()
    return result, check_pending_sync()

if __name__ == "__main__":
    # Jalankan sinkronisasi saat script dijalankan langsung
    run_auto_sync()