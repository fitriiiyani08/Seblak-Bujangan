import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys

# Tambahkan path ke root project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_data, save_data

# Konfigurasi halaman
st.set_page_config(
    page_title="Penjualan - Seblak Bujangan",
    page_icon="static/images/logo.jpeg",
    layout="wide"
)

# Custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static/styles.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css()

# Custom header
st.markdown("""
<div class="hero-section">
    <div class="hero-title">📊 Pencatatan Penjualan</div>
    <div class="hero-subtitle">Catat dan analisis penjualan Seblak Bujangan dengan mudah</div>
</div>
""", unsafe_allow_html=True)

# Load data
keuangan_df = load_data("data/keuangan.csv")
produk_df = load_data("data/produk.csv")

# Form pencatatan penjualan
st.markdown('<div class="fitur-header">✏️ Catat Penjualan Baru</div>', unsafe_allow_html=True)
st.markdown('<div class="form-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    produk = st.selectbox("Produk", produk_df['nama'].tolist())
    
    # Dapatkan harga produk
    harga = produk_df[produk_df['nama'] == produk]['harga'].values[0] if not produk_df.empty else 0
    st.write(f"Harga: Rp {harga:,.0f}".replace(",", "."))

with col2:
    jumlah_unit = st.number_input("Jumlah Unit", min_value=1, value=1)
    total_harga = harga * jumlah_unit
    st.write(f"Total: Rp {total_harga:,.0f}".replace(",", "."))

with col3:
    tanggal = st.date_input("Tanggal Penjualan", datetime.now())
    
    # Tambahkan tombol untuk menyimpan penjualan
    simpan_button = st.button("Simpan Penjualan")

if simpan_button:
    if not produk or jumlah_unit <= 0:
        st.error("Harap lengkapi semua field penjualan!")
    else:
        # Buat data penjualan baru
        new_sale = pd.DataFrame({
            'tanggal': [tanggal],
            'jenis': ['Pendapatan'],
            'kategori': ['Penjualan'],
            'deskripsi': [f"{produk} ({jumlah_unit} porsi)"],
            'jumlah': [total_harga]
        })
        
        # Tambahkan ke dataframe keuangan
        updated_df = pd.concat([keuangan_df, new_sale], ignore_index=True)
        
        # Simpan ke CSV
        save_data(updated_df, "data/keuangan.csv")
        
        st.success(f"Penjualan {produk} sebanyak {jumlah_unit} porsi berhasil dicatat!")
        st.balloons()
        
        # Reload data
        keuangan_df = load_data("data/keuangan.csv")
        
st.markdown('</div>', unsafe_allow_html=True)

# Tampilkan data penjualan
st.markdown("## 📋 Riwayat Penjualan")

# Filter untuk data penjualan saja
if not keuangan_df.empty:
    penjualan_df = keuangan_df[keuangan_df['jenis'] == 'Pendapatan']
    
    # Opsi filter tanggal
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Dari Tanggal", 
                               datetime.now() - timedelta(days=30),
                               key="penjualan_start_date")
    with col2:
        end_date = st.date_input("Sampai Tanggal", 
                             datetime.now(),
                             key="penjualan_end_date")
    
    # Filter berdasarkan tanggal
    if not penjualan_df.empty:
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        
        filtered_df = penjualan_df[(penjualan_df['tanggal'] >= start_date) & 
                                 (penjualan_df['tanggal'] <= end_date)]
    else:
        filtered_df = penjualan_df
    
    # Tampilkan tabel penjualan
    if not filtered_df.empty:
        # Konversi tanggal ke format yang lebih mudah dibaca
        display_df = filtered_df.copy()
        display_df['tanggal'] = display_df['tanggal'].dt.strftime('%d-%m-%Y')
        
        # Format kolom jumlah ke format Rupiah
        display_df['jumlah'] = display_df['jumlah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        
        # Tampilkan tabel
        st.dataframe(
            display_df[['tanggal', 'deskripsi', 'jumlah']],
            column_config={
                "tanggal": "Tanggal",
                "deskripsi": "Produk",
                "jumlah": "Total Harga"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Hitung total penjualan dalam periode
        total_penjualan = filtered_df['jumlah'].sum()
        st.success(f"Total Penjualan: Rp {total_penjualan:,.0f}".replace(",", "."))
        
        # Visualisasi tren penjualan harian
        st.markdown("## 📈 Tren Penjualan Harian")
        
        # Agregasi penjualan per hari
        daily_sales = filtered_df.groupby(filtered_df['tanggal'].dt.date)['jumlah'].sum().reset_index()
        daily_sales.columns = ['tanggal', 'total_penjualan']
        
        # Buat line chart
        fig = px.line(
            daily_sales, 
            x='tanggal', 
            y='total_penjualan',
            markers=True,
            title='Tren Penjualan Harian',
            color_discrete_sequence=['#e63946']
        )
        
        fig.update_layout(
            xaxis_title='Tanggal',
            yaxis_title='Total Penjualan (Rp)',
            hovermode='x unified'
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Visualisasi produk terlaris
        st.markdown("## 🏆 Produk Terlaris")
        
        # Ekstrak nama produk dari deskripsi dengan penanganan error
        try:
            filtered_df['nama_produk'] = filtered_df['deskripsi'].str.split(' (').str[0]
        except:
            # Jika format tidak sesuai, gunakan deskripsi asli
            if 'deskripsi' in filtered_df.columns:
                filtered_df['nama_produk'] = filtered_df['deskripsi']
            else:
                filtered_df['nama_produk'] = 'Produk'
        
        # Agregasi berdasarkan produk
        product_sales = filtered_df.groupby('nama_produk')['jumlah'].sum().reset_index()
        product_sales = product_sales.sort_values('jumlah', ascending=False)
        
        # Bar chart untuk produk terlaris
        fig = px.bar(
            product_sales,
            y='nama_produk',
            x='jumlah',
            orientation='h',
            color='jumlah',
            color_continuous_scale='Reds',
            title='Produk Terlaris berdasarkan Nilai Penjualan'
        )
        
        fig.update_layout(
            xaxis_title='Total Penjualan (Rp)',
            yaxis_title='Produk',
            yaxis={'categoryorder':'total ascending'},
            hovermode='y unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data penjualan dalam rentang tanggal yang dipilih.")
else:
    st.info("Belum ada data penjualan yang dicatat.")

# Tambahkan formulir untuk menambah produk baru
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="fitur-header">➕ Tambah Produk Baru</div>', unsafe_allow_html=True)
st.markdown('<div class="form-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    new_product_name = st.text_input("Nama Produk")

with col2:
    new_product_price = st.number_input("Harga (Rp)", min_value=0, step=1000)

with col3:
    st.write("")
    st.write("")
    add_product_button = st.button("Tambah Produk")

if add_product_button:
    if not new_product_name or new_product_price <= 0:
        st.error("Harap isi nama produk dan harga dengan benar!")
    else:
        # Check if product already exists
        if any(produk_df['nama'] == new_product_name):
            st.warning(f"Produk '{new_product_name}' sudah ada dalam daftar!")
        else:
            # Add new product
            new_product = pd.DataFrame({
                'nama': [new_product_name],
                'harga': [new_product_price]
            })
            
            # Concatenate with existing data
            updated_produk_df = pd.concat([produk_df, new_product], ignore_index=True)
            
            # Save to CSV
            save_data(updated_produk_df, "data/produk.csv")
            
            st.success(f"Produk '{new_product_name}' berhasil ditambahkan!")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
