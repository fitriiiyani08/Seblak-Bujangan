import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import time
import sys
import uuid

# Tambahkan path root ke sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import fungsi dari utils.py dan utils_pesanan.py
from utils import load_data, save_data
from utils_pesanan import (
    load_pesanan, save_pesanan, tambah_pesanan, get_pesanan_by_id, 
    update_status_pesanan, get_statistik_pesanan, get_pesanan_aktif,
    get_laporan_harian, get_produk_terlaris
)
from sync_data import check_pending_sync, manual_sync

# Fungsi untuk memuat CSS
def load_css():
    with open("static/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fungsi untuk membuat efek loading
def loading_effect():
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)  # Kecepatan loading
        progress_bar.progress(percent_complete + 1)
    time.sleep(0.5)
    progress_bar.empty()

# Fungsi untuk memuat data produk
def load_produk():
    file_path = "data/produk.csv"
    if os.path.exists(file_path):
        return load_data(file_path)
    else:
        # Buat file produk jika belum ada
        df = pd.DataFrame({
            'nama': ['Seblak Original', 'Seblak Seafood', 'Seblak Komplit', 'Seblak Mie'],
            'harga': [15000, 20000, 25000, 18000],
            'deskripsi': [
                'Seblak Original dengan kerupuk dan telur', 
                'Seblak dengan tambahan seafood (cumi, udang, dsb)', 
                'Seblak dengan semua topping', 
                'Seblak dengan tambahan mie'
            ]
        })
        save_data(df, file_path)
        return df

# Fungsi untuk menyimpan pesanan baru
def simpan_pesanan(pesanan_data):
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
    save_data(pesanan_df, "data/pesanan.csv")
    return pesanan_id

# Inisialisasi aplikasi
st.set_page_config(
    page_title="Seblak Bujangan - Pencatatan Pesanan",
    page_icon="🌶️",
    layout="wide"
)

# Load CSS
load_css()

# Judul Halaman
st.markdown('<h1 class="red-text">Pencatatan Pesanan</h1>', unsafe_allow_html=True)
st.markdown('<div class="red-shadow"></div>', unsafe_allow_html=True)

# Tab untuk membagi tampilan
tab1, tab2, tab3 = st.tabs(["Tambah Pesanan", "Pesanan Aktif", "Riwayat Pesanan"])

# Tambah Pesanan (Tab 1)
with tab1:
    st.markdown('<h3 class="cream-text">Tambah Pesanan Baru</h3>', unsafe_allow_html=True)
    
    # Form untuk menambah pesanan
    col1, col2 = st.columns(2)
    
    with col1:
        nama_pembeli = st.text_input("Nama Pembeli")
        
        # Load produk untuk dipilih
        produk_df = load_produk()
        produk_list = produk_df['nama'].tolist()
        produk_list.append("Prasmanan/Custom")
        
        produk = st.selectbox("Produk", produk_list)
        jumlah = st.number_input("Jumlah", min_value=1, value=1)
        
        # Harga total berdasarkan inputan manual untuk sistem prasmanan
        if produk == "Prasmanan/Custom":
            custom_produk = st.text_input("Detail Pesanan Prasmanan", 
                placeholder="Mis: Seblak Prasmanan + 2 Bakso + 3 Ceker")
            harga_total = st.number_input("Harga Total (Rp)", min_value=0, step=1000, value=15000)
            if custom_produk:
                produk = f"Custom: {custom_produk}"
            else:
                produk = "Prasmanan"
        else:
            # Hitung harga berdasarkan menu tetap
            harga_dict = dict(zip(produk_df['nama'], produk_df['harga']))
            harga_satuan = harga_dict[produk]
            
            # Input harga manual jika ada perubahan harga
            use_manual_price = st.checkbox("Ubah harga?", help="Centang jika ingin mengubah harga")
            
            if use_manual_price:
                harga_total = st.number_input("Harga Total (Rp)", min_value=0, step=1000, value=harga_satuan * jumlah)
            else:
                harga_total = harga_satuan * jumlah
                st.write(f"Harga Total: Rp {harga_total:,.0f}")
        
        tingkat_kepedasan = st.select_slider(
            "Tingkat Kepedasan", 
            options=["Tidak Pedas", "Sedikit Pedas", "Sedang", "Pedas", "Sangat Pedas"]
        )
    
    with col2:
        catatan = st.text_area("Catatan Tambahan", height=100)
        
        metode_pembayaran = st.selectbox(
            "Metode Pembayaran",
            ["Tunai", "QRIS", "Transfer Bank", "OVO", "GoPay", "ShopeePay", "Dana"]
        )
        
        tipe_pesanan = st.radio("Tipe Pesanan", ["Dine In", "Take Away"])
        
        status_pesanan = "Dalam Proses"  # Default status untuk pesanan baru
    
    # Tombol untuk menyimpan pesanan
    if st.button("Simpan Pesanan", type="primary"):
        if not nama_pembeli or not produk:
            st.error("Nama pembeli dan produk harus diisi!")
        else:
            # Siapkan data pesanan
            pesanan_data = {
                'nama_pembeli': nama_pembeli,
                'produk': produk,
                'jumlah': jumlah,
                'harga_total': harga_total,
                'tingkat_kepedasan': tingkat_kepedasan,
                'catatan': catatan,
                'metode_pembayaran': metode_pembayaran,
                'status_pesanan': status_pesanan,
                'tipe_pesanan': tipe_pesanan,
                'waktu_selesai': None
            }
            
            # Efek loading saat menyimpan
            with st.spinner("Menyimpan pesanan..."):
                loading_effect()
                pesanan_id = simpan_pesanan(pesanan_data)
            
            # Notifikasi sukses
            st.success(f"Pesanan berhasil disimpan dengan ID: {pesanan_id}")
            st.balloons()  # Efek balon sebagai perayaan
            
            # Reset form
            st.rerun()

# Pesanan Aktif (Tab 2)
with tab2:
    st.markdown('<h3 class="cream-text">Pesanan Aktif</h3>', unsafe_allow_html=True)
    
    # Tambahkan tombol refresh
    if st.button("Refresh Daftar Pesanan", key="refresh_active"):
        st.rerun()
    
    # Dapatkan dan tampilkan pesanan aktif
    pesanan_aktif = get_pesanan_aktif()
    
    if len(pesanan_aktif) == 0:
        st.info("Tidak ada pesanan aktif saat ini.")
    else:
        # Tampilkan pesanan aktif dalam bentuk kartu
        for i, pesanan in pesanan_aktif.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"<div class='pesanan-card'>", unsafe_allow_html=True)
                    st.markdown(f"<h4>ID: {pesanan['id']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Pembeli:</b> {pesanan['nama_pembeli']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Produk:</b> {pesanan['produk']} x {pesanan['jumlah']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Total:</b> Rp {pesanan['harga_total']:,.0f}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"<div class='pesanan-card'>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Kepedasan:</b> {pesanan['tingkat_kepedasan']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Catatan:</b> {pesanan['catatan']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Metode Pembayaran:</b> {pesanan['metode_pembayaran']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Tipe:</b> {pesanan['tipe_pesanan']}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"<div class='pesanan-card status-card'>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Status:</b> {pesanan['status_pesanan']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p><b>Waktu Pesan:</b> {pesanan['waktu_pemesanan']}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Tombol untuk mengubah status
                    if pesanan['status_pesanan'] == "Dalam Proses":
                        if st.button("Tandai Siap", key=f"siap_{pesanan['id']}"):
                            update_status_pesanan(pesanan['id'], "Siap")
                            st.success("Status pesanan berhasil diubah!")
                            time.sleep(1)
                            st.rerun()
                    
                    if pesanan['status_pesanan'] in ["Dalam Proses", "Siap"]:
                        if st.button("Tandai Selesai", key=f"selesai_{pesanan['id']}"):
                            update_status_pesanan(pesanan['id'], "Selesai")
                            
                            # Sinkronisasi dengan penjualan dan laporan
                            with st.spinner("Menyinkronkan dengan data penjualan..."):
                                result, _ = manual_sync()
                                if result:
                                    st.success("Pesanan selesai dan sudah disinkronkan dengan data penjualan!")
                                else:
                                    st.warning("Pesanan selesai, tetapi gagal sinkronisasi. Coba lagi nanti.")
                            
                            time.sleep(1)
                            st.rerun()
            
            st.markdown("<hr>", unsafe_allow_html=True)

# Riwayat Pesanan (Tab 3)
with tab3:
    st.markdown('<h3 class="cream-text">Riwayat Pesanan</h3>', unsafe_allow_html=True)
    
    # Tambahkan tombol sinkronisasi manual
    pending_count = check_pending_sync()
    if pending_count > 0:
        if st.button(f"🔄 Sinkronkan {pending_count} Pesanan ke Data Penjualan", type="primary"):
            with st.spinner("Menyinkronkan pesanan ke data penjualan..."):
                result, remaining = manual_sync()
                if result:
                    if remaining == 0:
                        st.success("Semua pesanan berhasil disinkronkan ke data penjualan!")
                    else:
                        st.warning(f"Beberapa pesanan berhasil disinkronkan, tetapi masih ada {remaining} pesanan yang belum.")
                else:
                    st.error("Gagal menyinkronkan pesanan. Coba lagi nanti.")
    else:
        st.info("Semua pesanan sudah disinkronkan dengan data penjualan.")
    
    # Filter tanggal
    col1, col2 = st.columns(2)
    with col1:
        tanggal_awal = st.date_input("Tanggal Awal", datetime.now())
    with col2:
        tanggal_akhir = st.date_input("Tanggal Akhir", datetime.now())
    
    # Load data pesanan
    pesanan_df = load_pesanan()
    
    # Filter berdasarkan tanggal
    if not pesanan_df.empty and 'tanggal' in pesanan_df.columns:
        pesanan_df['tanggal'] = pd.to_datetime(pesanan_df['tanggal']).dt.date
        mask = (pesanan_df['tanggal'] >= tanggal_awal) & (pesanan_df['tanggal'] <= tanggal_akhir)
        filtered_df = pesanan_df[mask]
        
        if filtered_df.empty:
            st.info(f"Tidak ada pesanan dalam rentang tanggal {tanggal_awal} sampai {tanggal_akhir}")
        else:
            # Tampilkan data
            st.markdown("<div class='table-container'>", unsafe_allow_html=True)
            
            # Sorting dan pemilihan kolom untuk tampilan
            display_columns = [
                'id', 'tanggal', 'nama_pembeli', 'produk', 'jumlah', 'harga_total',
                'tingkat_kepedasan', 'metode_pembayaran', 'status_pesanan', 'tipe_pesanan'
            ]
            
            # Pastikan semua kolom ada
            display_columns = [col for col in display_columns if col in filtered_df.columns]
            
            # Sort berdasarkan tanggal terbaru
            if 'tanggal' in filtered_df.columns and 'waktu_pemesanan' in filtered_df.columns:
                sorted_df = filtered_df.sort_values(by=['tanggal', 'waktu_pemesanan'], ascending=[False, False])
            else:
                sorted_df = filtered_df
            
            # Format tampilan DataFrame
            formatted_df = sorted_df[display_columns].copy()
            if 'harga_total' in formatted_df.columns:
                formatted_df['harga_total'] = formatted_df['harga_total'].apply(lambda x: f"Rp {x:,.0f}")
            
            st.dataframe(
                formatted_df,
                use_container_width=True,
                height=400
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Informasi total
            total_penjualan = filtered_df['harga_total'].sum()
            total_pesanan = len(filtered_df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Pesanan", total_pesanan)
            with col2:
                st.metric("Total Pendapatan", f"Rp {total_penjualan:,.0f}")
                
            # Unduh data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download Data (CSV)",
                data=csv,
                file_name=f"pesanan_{tanggal_awal}_{tanggal_akhir}.csv",
                mime="text/csv"
            )
    else:
        st.info("Belum ada data pesanan.")

# Tambahan CSS untuk styling pesanan
st.markdown("""
<style>
.pesanan-card {
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 5px;
    background-color: rgba(255, 245, 238, 0.9);
    color: #333;
}

.status-card {
    background-color: rgba(255, 99, 71, 0.1);
}

hr {
    margin: 20px 0;
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(255, 99, 71, 0), rgba(255, 99, 71, 0.75), rgba(255, 99, 71, 0));
}

.table-container {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px;
    border-radius: 5px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)