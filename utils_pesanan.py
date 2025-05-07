"""
Utilitas untuk mengelola transaksi pesanan dengan dukungan harga yang fleksibel
untuk sistem prasmanan dan pesanan khusus Seblak Bujangan.
"""

import pandas as pd
import os
from datetime import datetime
import uuid

# Fungsi untuk memuat data
def load_pesanan():
    """
    Memuat data pesanan dari CSV file
    """
    file_path = "data/pesanan.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Buat file baru dengan kolom yang sesuai
        df = pd.DataFrame(columns=[
            'id', 'tanggal', 'nama_pembeli', 'produk', 'jumlah', 'harga_total', 
            'tingkat_kepedasan', 'catatan', 'metode_pembayaran', 'status_pesanan', 
            'tipe_pesanan', 'waktu_pemesanan', 'waktu_selesai'
        ])
        df.to_csv(file_path, index=False)
        return df

# Fungsi untuk menyimpan data pesanan
def save_pesanan(df):
    """
    Menyimpan dataframe pesanan ke CSV file
    """
    file_path = "data/pesanan.csv"
    df.to_csv(file_path, index=False)

# Fungsi untuk menambahkan pesanan baru
def tambah_pesanan(pesanan_data):
    """
    Menambahkan pesanan baru ke database
    
    Parameters:
    -----------
    pesanan_data : dict
        Dictionary berisi data pesanan (nama_pembeli, produk, jumlah, dll)
        
    Returns:
    --------
    str : ID pesanan yang baru dibuat
    """
    pesanan_df = load_pesanan()
    
    # Buat ID unik untuk pesanan baru
    pesanan_id = str(uuid.uuid4())[:8]
    
    # Tambahkan ID dan tanggal ke pesanan_data
    pesanan_data['id'] = pesanan_id
    pesanan_data['tanggal'] = datetime.now().strftime('%Y-%m-%d')
    pesanan_data['waktu_pemesanan'] = datetime.now().strftime('%H:%M:%S')
    
    # Tambahkan pesanan baru ke DataFrame
    pesanan_df = pd.concat([pesanan_df, pd.DataFrame([pesanan_data])], ignore_index=True)
    
    # Simpan perubahan
    save_pesanan(pesanan_df)
    return pesanan_id

# Fungsi untuk mendapatkan pesanan berdasarkan ID
def get_pesanan_by_id(pesanan_id):
    """
    Mendapatkan data pesanan berdasarkan ID
    
    Parameters:
    -----------
    pesanan_id : str
        ID pesanan yang ingin dicari
        
    Returns:
    --------
    pd.Series : Data pesanan, atau None jika pesanan tidak ditemukan
    """
    pesanan_df = load_pesanan()
    if pesanan_id in pesanan_df['id'].values:
        return pesanan_df[pesanan_df['id'] == pesanan_id].iloc[0]
    return None

# Fungsi untuk memperbarui status pesanan
def update_status_pesanan(pesanan_id, status_baru, waktu_selesai=None):
    """
    Memperbarui status pesanan
    
    Parameters:
    -----------
    pesanan_id : str
        ID pesanan yang ingin diubah statusnya
    status_baru : str
        Status baru pesanan ('Dalam Proses', 'Siap', 'Selesai')
    waktu_selesai : str, optional
        Waktu penyelesaian pesanan, diisi otomatis jika None dan status='Selesai'
        
    Returns:
    --------
    bool : True jika update berhasil, False jika gagal
    """
    pesanan_df = load_pesanan()
    if pesanan_id in pesanan_df['id'].values:
        idx = pesanan_df[pesanan_df['id'] == pesanan_id].index[0]
        pesanan_df.at[idx, 'status_pesanan'] = status_baru
        
        if status_baru == "Selesai" and waktu_selesai is None:
            waktu_selesai = datetime.now().strftime('%H:%M:%S')
        
        if waktu_selesai:
            pesanan_df.at[idx, 'waktu_selesai'] = waktu_selesai
            
        save_pesanan(pesanan_df)
        return True
    return False

# Fungsi untuk mendapatkan statistik pesanan
def get_statistik_pesanan(start_date=None, end_date=None):
    """
    Mendapatkan statistik pesanan dalam rentang tanggal tertentu
    
    Parameters:
    -----------
    start_date : str, optional
        Tanggal awal dalam format YYYY-MM-DD
    end_date : str, optional
        Tanggal akhir dalam format YYYY-MM-DD
        
    Returns:
    --------
    dict : Statistik pesanan (total_pesanan, total_pendapatan, rata2_harga, dll)
    """
    pesanan_df = load_pesanan()
    
    if pesanan_df.empty:
        return {
            'total_pesanan': 0,
            'total_pendapatan': 0,
            'rata2_harga': 0,
            'produk_terlaris': 'Belum ada',
            'pesanan_termahal': 0
        }
    
    # Filter berdasarkan tanggal jika diberikan
    if start_date and end_date:
        pesanan_df['tanggal'] = pd.to_datetime(pesanan_df['tanggal'])
        pesanan_df = pesanan_df[(pesanan_df['tanggal'] >= start_date) & 
                               (pesanan_df['tanggal'] <= end_date)]
    
    # Hitung statistik
    if not pesanan_df.empty:
        # Produk terlaris
        produk_count = pesanan_df['produk'].value_counts()
        produk_terlaris = produk_count.index[0] if not produk_count.empty else 'Belum ada'
        
        # Statistik lainnya
        return {
            'total_pesanan': len(pesanan_df),
            'total_pendapatan': pesanan_df['harga_total'].sum(),
            'rata2_harga': pesanan_df['harga_total'].mean(),
            'produk_terlaris': produk_terlaris,
            'pesanan_termahal': pesanan_df['harga_total'].max()
        }
    else:
        return {
            'total_pesanan': 0,
            'total_pendapatan': 0,
            'rata2_harga': 0,
            'produk_terlaris': 'Belum ada',
            'pesanan_termahal': 0
        }

# Fungsi untuk mendapatkan daftar pesanan aktif
def get_pesanan_aktif():
    """
    Mendapatkan daftar pesanan yang belum selesai
    
    Returns:
    --------
    pd.DataFrame : DataFrame berisi pesanan yang belum selesai
    """
    pesanan_df = load_pesanan()
    
    # Filter pesanan yang belum selesai
    return pesanan_df[pesanan_df['status_pesanan'] != "Selesai"].sort_values(by='waktu_pemesanan')

# Fungsi untuk mendapatkan laporan pesanan harian
def get_laporan_harian(tanggal):
    """
    Mendapatkan laporan pesanan untuk tanggal tertentu
    
    Parameters:
    -----------
    tanggal : str
        Tanggal dalam format YYYY-MM-DD
        
    Returns:
    --------
    dict : Laporan pesanan harian
    """
    pesanan_df = load_pesanan()
    if pesanan_df.empty:
        return {
            'tanggal': tanggal,
            'total_pesanan': 0,
            'total_pendapatan': 0,
            'dine_in': 0,
            'take_away': 0
        }
    
    # Filter berdasarkan tanggal
    pesanan_df['tanggal'] = pd.to_datetime(pesanan_df['tanggal']).dt.strftime('%Y-%m-%d')
    day_df = pesanan_df[pesanan_df['tanggal'] == tanggal]
    
    if day_df.empty:
        return {
            'tanggal': tanggal,
            'total_pesanan': 0,
            'total_pendapatan': 0,
            'dine_in': 0,
            'take_away': 0
        }
    
    # Hitung statistik
    dine_in_count = len(day_df[day_df['tipe_pesanan'] == 'Dine In'])
    take_away_count = len(day_df[day_df['tipe_pesanan'] == 'Take Away'])
    
    return {
        'tanggal': tanggal,
        'total_pesanan': len(day_df),
        'total_pendapatan': day_df['harga_total'].sum(),
        'dine_in': dine_in_count,
        'take_away': take_away_count
    }

# Fungsi untuk mendapatkan laporan produk terlaris
def get_produk_terlaris(start_date=None, end_date=None, limit=5):
    """
    Mendapatkan daftar produk terlaris dalam rentang tanggal
    
    Parameters:
    -----------
    start_date : str, optional
        Tanggal awal dalam format YYYY-MM-DD
    end_date : str, optional
        Tanggal akhir dalam format YYYY-MM-DD
    limit : int, optional
        Jumlah produk terlaris yang ingin ditampilkan
        
    Returns:
    --------
    pd.DataFrame : DataFrame berisi produk terlaris dengan kolom produk dan jumlah
    """
    pesanan_df = load_pesanan()
    
    if pesanan_df.empty:
        return pd.DataFrame(columns=['produk', 'jumlah', 'pendapatan'])
    
    # Filter berdasarkan tanggal jika diberikan
    if start_date and end_date:
        pesanan_df['tanggal'] = pd.to_datetime(pesanan_df['tanggal'])
        pesanan_df = pesanan_df[(pesanan_df['tanggal'] >= start_date) & 
                               (pesanan_df['tanggal'] <= end_date)]
    
    # Hitung produk terlaris berdasarkan jumlah pesanan
    if not pesanan_df.empty:
        # Ekstrak nama produk (gunakan split jika produk berformat 'Custom: ...')
        pesanan_df['nama_produk'] = pesanan_df['produk'].apply(
            lambda x: x.split('Custom: ')[-1] if 'Custom: ' in x else x
        )
        
        # Agregasi berdasarkan produk
        produk_count = pesanan_df.groupby('nama_produk').agg({
            'jumlah': 'sum',
            'harga_total': 'sum'
        }).reset_index()
        
        produk_count.columns = ['produk', 'jumlah', 'pendapatan']
        produk_count = produk_count.sort_values('jumlah', ascending=False).head(limit)
        
        return produk_count
    else:
        return pd.DataFrame(columns=['produk', 'jumlah', 'pendapatan'])