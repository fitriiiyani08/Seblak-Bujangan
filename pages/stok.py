import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import sys

# Tambahkan path ke root project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_data, save_data

# Konfigurasi halaman
st.set_page_config(
    page_title="Stok Bahan - Seblak Bujangan",
    page_icon="🍜",
    layout="wide"
)

# Judul halaman
st.title("📦 Manajemen Stok Bahan")
st.markdown("Halaman ini untuk mencatat dan mengelola stok bahan untuk Seblak Bujangan.")

# Load data
bahan_df = load_data("data/bahan.csv")
keuangan_df = load_data("data/keuangan.csv")

# Tampilkan stok bahan saat ini
st.markdown("## 📋 Stok Bahan Saat Ini")

if not bahan_df.empty:
    # Tambahkan kolom status stok
    bahan_df['status'] = bahan_df['stok'].apply(
        lambda x: "⚠️ Hampir Habis" if x <= 3 else "✅ Tersedia"
    )
    
    # Format tampilan
    display_df = bahan_df.copy()
    display_df['stok'] = display_df.apply(
        lambda row: f"{row['stok']} {row['satuan']}", axis=1
    )
    
    # Tampilkan tabel
    st.dataframe(
        display_df[['nama', 'stok', 'status']],
        column_config={
            "nama": "Nama Bahan",
            "stok": "Jumlah Stok",
            "status": "Status"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Visualisasi stok bahan
    st.markdown("### 📊 Visualisasi Stok Bahan")
    
    # Bar chart untuk stok bahan
    fig = px.bar(
        bahan_df.sort_values('stok', ascending=True),
        y='nama',
        x='stok',
        orientation='h',
        color='stok',
        color_continuous_scale='Reds_r',  # Reverse Reds colorscale to show low stock in red
        title='Stok Bahan Saat Ini',
        text='stok'
    )
    
    fig.update_layout(
        xaxis_title='Jumlah Stok',
        yaxis_title='Nama Bahan',
        hovermode='y unified'
    )
    
    # Menampilkan nilai stok di dalam bar
    fig.update_traces(
        texttemplate='%{text}',
        textposition='inside'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tampilkan peringatan untuk bahan yang hampir habis
    low_stock = bahan_df[bahan_df['stok'] <= 3]
    if not low_stock.empty:
        st.warning("⚠️ Beberapa bahan hampir habis! Segera lakukan pembelian.")
        
        # Tampilkan daftar bahan yang hampir habis
        st.dataframe(
            low_stock[['nama', 'stok']],
            column_config={
                "nama": "Nama Bahan",
                "stok": "Jumlah Stok"
            },
            hide_index=True,
            use_container_width=True
        )
else:
    st.info("Belum ada data stok bahan yang tersedia.")

# Form untuk menambah/update stok bahan
st.markdown("## ➕ Tambah/Update Stok Bahan")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Opsi untuk memilih bahan yang sudah ada atau menambah bahan baru
    option = st.radio("Pilih opsi:", ["Update Stok Bahan", "Tambah Bahan Baru"])
    
    if option == "Update Stok Bahan":
        if not bahan_df.empty:
            bahan_nama = st.selectbox("Pilih Bahan", bahan_df['nama'].tolist())
        else:
            st.error("Belum ada data bahan. Silakan tambahkan bahan baru terlebih dahulu.")
            bahan_nama = None
    else:
        bahan_nama = st.text_input("Nama Bahan Baru")

with col2:
    if option == "Update Stok Bahan" and bahan_nama:
        current_stok = bahan_df[bahan_df['nama'] == bahan_nama]['stok'].values[0]
        current_satuan = bahan_df[bahan_df['nama'] == bahan_nama]['satuan'].values[0]
        
        st.write(f"Stok Saat Ini: {current_stok} {current_satuan}")
        
        aksi = st.radio("Aksi:", ["Tambah Stok", "Kurangi Stok"])
        jumlah = st.number_input("Jumlah", min_value=0.1, step=0.1, format="%.1f")
    else:
        stok_awal = st.number_input("Stok Awal", min_value=0.0, step=0.1, format="%.1f")

with col3:
    if option == "Tambah Bahan Baru":
        satuan = st.selectbox("Satuan", ["kg", "liter", "buah", "pack", "lusin", "kotak"])
    elif option == "Update Stok Bahan" and bahan_nama:
        # Tampilkan satuan yang sudah ada
        st.write(f"Satuan: {current_satuan}")
        
        # Jika aksi adalah tambah stok, minta harga pembelian
        if aksi == "Tambah Stok":
            harga_pembelian = st.number_input("Harga Pembelian (Rp)", min_value=0, step=1000)

with col4:
    st.write("")
    st.write("")
    simpan_button = st.button("Simpan Perubahan")

if simpan_button:
    if option == "Update Stok Bahan" and bahan_nama:
        # Update stok bahan yang sudah ada
        if aksi == "Tambah Stok":
            if jumlah <= 0:
                st.error("Jumlah harus lebih dari 0!")
            else:
                # Update stok
                bahan_df.loc[bahan_df['nama'] == bahan_nama, 'stok'] += jumlah
                
                # Catat pembelian bahan ke data keuangan jika ada harga pembelian
                if 'harga_pembelian' in locals() and harga_pembelian > 0:
                    new_expense = pd.DataFrame({
                        'tanggal': [datetime.now()],
                        'jenis': ['Pengeluaran'],
                        'kategori': ['Bahan Baku'],
                        'deskripsi': [f"Pembelian {bahan_nama} ({jumlah} {current_satuan})"],
                        'jumlah': [harga_pembelian]
                    })
                    
                    # Tambahkan ke dataframe keuangan
                    updated_keuangan_df = pd.concat([keuangan_df, new_expense], ignore_index=True)
                    
                    # Simpan ke CSV
                    save_data(updated_keuangan_df, "data/keuangan.csv")
                
                # Simpan perubahan stok
                save_data(bahan_df, "data/bahan.csv")
                
                st.success(f"Stok {bahan_nama} berhasil ditambahkan menjadi {bahan_df.loc[bahan_df['nama'] == bahan_nama, 'stok'].values[0]} {current_satuan}!")
                st.rerun()
        else:  # Kurangi Stok
            if jumlah <= 0:
                st.error("Jumlah harus lebih dari 0!")
            elif jumlah > current_stok:
                st.error(f"Jumlah pengurangan ({jumlah}) melebihi stok saat ini ({current_stok})!")
            else:
                # Update stok
                bahan_df.loc[bahan_df['nama'] == bahan_nama, 'stok'] -= jumlah
                
                # Simpan perubahan
                save_data(bahan_df, "data/bahan.csv")
                
                st.success(f"Stok {bahan_nama} berhasil dikurangi menjadi {bahan_df.loc[bahan_df['nama'] == bahan_nama, 'stok'].values[0]} {current_satuan}!")
                st.rerun()
    
    else:  # Tambah Bahan Baru
        if not bahan_nama:
            st.error("Nama bahan tidak boleh kosong!")
        elif stok_awal < 0:
            st.error("Stok awal tidak boleh negatif!")
        elif bahan_df.empty or bahan_nama not in bahan_df['nama'].values:
            # Tambah bahan baru
            new_bahan = pd.DataFrame({
                'nama': [bahan_nama],
                'stok': [stok_awal],
                'satuan': [satuan]
            })
            
            # Gabungkan dengan data yang ada
            updated_bahan_df = pd.concat([bahan_df, new_bahan], ignore_index=True)
            
            # Simpan ke CSV
            save_data(updated_bahan_df, "data/bahan.csv")
            
            st.success(f"Bahan baru '{bahan_nama}' berhasil ditambahkan dengan stok awal {stok_awal} {satuan}!")
            st.rerun()
        else:
            st.error(f"Bahan dengan nama '{bahan_nama}' sudah ada!")

# Form untuk pengambilan stok untuk produksi
st.markdown("## 🔄 Pengambilan Stok untuk Produksi")

col1, col2, col3 = st.columns(3)

with col1:
    if not bahan_df.empty:
        produksi_bahan = st.selectbox("Pilih Bahan", bahan_df['nama'].tolist(), key="produksi_bahan")
        current_stok = bahan_df[bahan_df['nama'] == produksi_bahan]['stok'].values[0]
        current_satuan = bahan_df[bahan_df['nama'] == produksi_bahan]['satuan'].values[0]
        
        st.write(f"Stok Saat Ini: {current_stok} {current_satuan}")
    else:
        st.error("Belum ada data bahan. Silakan tambahkan bahan terlebih dahulu.")
        produksi_bahan = None

with col2:
    if produksi_bahan:
        produksi_jumlah = st.number_input("Jumlah yang Diambil", min_value=0.1, max_value=float(current_stok), step=0.1, format="%.1f")
        produksi_catatan = st.text_input("Catatan (opsional)", placeholder="Misal: untuk 50 porsi seblak")

with col3:
    st.write("")
    st.write("")
    ambil_button = st.button("Ambil untuk Produksi")

if ambil_button and produksi_bahan:
    if produksi_jumlah <= 0:
        st.error("Jumlah harus lebih dari 0!")
    elif produksi_jumlah > current_stok:
        st.error(f"Jumlah pengambilan ({produksi_jumlah}) melebihi stok saat ini ({current_stok})!")
    else:
        # Update stok
        bahan_df.loc[bahan_df['nama'] == produksi_bahan, 'stok'] -= produksi_jumlah
        
        # Simpan perubahan
        save_data(bahan_df, "data/bahan.csv")
        
        # Buat catatan lengkap
        catatan = f"Produksi: {produksi_bahan} ({produksi_jumlah} {current_satuan})"
        if produksi_catatan:
            catatan += f" - {produksi_catatan}"
            
        st.success(f"Berhasil mengambil {produksi_jumlah} {current_satuan} {produksi_bahan} untuk produksi.")
        st.success(f"Stok {produksi_bahan} sekarang: {bahan_df.loc[bahan_df['nama'] == produksi_bahan, 'stok'].values[0]} {current_satuan}!")
        st.rerun()
