import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from utils import load_data, save_data, calculate_profit_loss, get_summary

# Konfigurasi halaman
st.set_page_config(
    page_title="Keuangan Seblak Bujangan",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Judul aplikasi
st.title("📊 Manajemen Keuangan Seblak Bujangan")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/noodles.png", width=100)
    st.header("Seblak Bujangan")
    st.markdown("---")
    st.markdown("### Menu Navigasi")
    
# Inisialisasi data
if 'data_initialized' not in st.session_state:
    # Pastikan direktori data ada
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Inisialisasi file keuangan jika belum ada
    if not os.path.exists("data/keuangan.csv"):
        keuangan_df = pd.DataFrame({
            'tanggal': [],
            'jenis': [],
            'kategori': [],
            'deskripsi': [],
            'jumlah': []
        })
        keuangan_df.to_csv("data/keuangan.csv", index=False)
    
    # Inisialisasi file produk jika belum ada
    if not os.path.exists("data/produk.csv"):
        produk_df = pd.DataFrame({
            'nama': ["Seblak Original", "Seblak Spesial", "Seblak Seafood", "Seblak Tulang", "Mie Instan"],
            'harga': [15000, 20000, 25000, 18000, 10000]
        })
        produk_df.to_csv("data/produk.csv", index=False)
    
    # Inisialisasi file bahan jika belum ada
    if not os.path.exists("data/bahan.csv"):
        bahan_df = pd.DataFrame({
            'nama': ["Kerupuk", "Mie", "Telur", "Bumbu", "Sayuran", "Bakso", "Sosis", "Seafood"],
            'stok': [10, 20, 30, 5, 3, 15, 15, 10],
            'satuan': ["kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg"]
        })
        bahan_df.to_csv("data/bahan.csv", index=False)
        
    st.session_state.data_initialized = True

# Load data
keuangan_df = load_data("data/keuangan.csv")

# DASHBOARD UTAMA

# Dapatkan data bulan ini
today = datetime.now()
start_of_month = datetime(today.year, today.month, 1)
end_of_month = (datetime(today.year, today.month + 1, 1) if today.month < 12 
                else datetime(today.year + 1, 1, 1)) - timedelta(days=1)

# Filter data untuk bulan ini
if not keuangan_df.empty:
    keuangan_df['tanggal'] = pd.to_datetime(keuangan_df['tanggal'])
    month_data = keuangan_df[(keuangan_df['tanggal'] >= start_of_month) & 
                             (keuangan_df['tanggal'] <= end_of_month)]
else:
    month_data = keuangan_df

# Tampilkan metrik utama
st.subheader("📌 Ringkasan Bulan Ini")
col1, col2, col3, col4 = st.columns(4)

# Dapatkan summary data keuangan
summary = get_summary(month_data)

with col1:
    st.metric(
        label="Total Penjualan",
        value=f"Rp {summary['pendapatan']:,.0f}".replace(",", ".")
    )

with col2:
    st.metric(
        label="Total Pengeluaran",
        value=f"Rp {summary['pengeluaran']:,.0f}".replace(",", ".")
    )

with col3:
    profit_loss = summary['pendapatan'] - summary['pengeluaran']
    st.metric(
        label="Keuntungan/Kerugian",
        value=f"Rp {profit_loss:,.0f}".replace(",", "."),
        delta=f"{profit_loss/summary['pendapatan']*100:.1f}%" if summary['pendapatan'] > 0 else "0%"
    )

with col4:
    st.metric(
        label="Transaksi",
        value=f"{summary['transaksi']} kali"
    )

# Tampilkan grafik tren pendapatan & pengeluaran
st.subheader("📈 Tren Keuangan (7 Hari Terakhir)")

# Dapatkan data 7 hari terakhir
end_date = datetime.now()
start_date = end_date - timedelta(days=6)

if not keuangan_df.empty:
    # Filter data untuk 7 hari terakhir
    last_7_days = keuangan_df[(keuangan_df['tanggal'] >= start_date) & 
                              (keuangan_df['tanggal'] <= end_date)]
    
    # Buat dataframe harian dengan semua tanggal dari 7 hari terakhir
    date_range = pd.date_range(start=start_date, end=end_date)
    daily_data = pd.DataFrame({'tanggal': date_range})
    
    # Agregasi berdasarkan tanggal dan jenis
    if not last_7_days.empty:
        daily_summary = last_7_days.groupby(['tanggal', 'jenis'])['jumlah'].sum().reset_index()
    
        # Pivot table untuk memisahkan pendapatan dan pengeluaran
        pivot_data = daily_summary.pivot_table(
            index='tanggal', 
            columns='jenis', 
            values='jumlah', 
            aggfunc='sum'
        ).reset_index()
        
        # Merge dengan range tanggal untuk memastikan semua tanggal ada
        daily_data = pd.merge(daily_data, pivot_data, on='tanggal', how='left')
    else:
        daily_data['Pendapatan'] = 0
        daily_data['Pengeluaran'] = 0
    
    # Isi NaN dengan 0
    daily_data = daily_data.fillna(0)
    
    # Format tanggal untuk tampilan
    daily_data['tanggal_str'] = daily_data['tanggal'].dt.strftime('%d %b')
    
    # Buat grafik
    fig = go.Figure()
    
    if 'Pendapatan' in daily_data.columns:
        fig.add_trace(go.Scatter(
            x=daily_data['tanggal_str'], 
            y=daily_data['Pendapatan'],
            mode='lines+markers',
            name='Pendapatan',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=8)
        ))
    
    if 'Pengeluaran' in daily_data.columns:
        fig.add_trace(go.Scatter(
            x=daily_data['tanggal_str'], 
            y=daily_data['Pengeluaran'],
            mode='lines+markers',
            name='Pengeluaran',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        xaxis_title='Tanggal',
        yaxis_title='Jumlah (Rp)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=30, b=0),
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Belum ada data keuangan untuk ditampilkan.")

# Tampilkan Distribusi Kategori Pengeluaran
if not keuangan_df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥧 Distribusi Pengeluaran")
        
        # Filter data pengeluaran bulan ini
        pengeluaran_df = month_data[month_data['jenis'] == 'Pengeluaran']
        
        if not pengeluaran_df.empty:
            # Agregasi berdasarkan kategori
            kategori_agg = pengeluaran_df.groupby('kategori')['jumlah'].sum().reset_index()
            
            # Buat pie chart
            fig = px.pie(
                kategori_agg, 
                values='jumlah', 
                names='kategori',
                color_discrete_sequence=px.colors.sequential.Reds,
                hole=0.4
            )
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=20, b=0),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data pengeluaran bulan ini.")
    
    with col2:
        st.subheader("🏆 Produk Terlaris")
        
        # Filter data pendapatan bulan ini
        pendapatan_df = month_data[month_data['jenis'] == 'Pendapatan']
        
        if not pendapatan_df.empty:
            # Agregasi berdasarkan produk (deskripsi)
            produk_agg = pendapatan_df.groupby('deskripsi')['jumlah'].sum().reset_index()
            
            # Urutkan
            produk_agg = produk_agg.sort_values('jumlah', ascending=False).head(5)
            
            # Bar chart
            fig = px.bar(
                produk_agg,
                x='jumlah',
                y='deskripsi',
                orientation='h',
                color='jumlah',
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(
                xaxis_title='Pendapatan (Rp)',
                yaxis_title='',
                margin=dict(l=0, r=0, t=20, b=0),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data penjualan bulan ini.")

st.markdown("---")

# Tambah pencatatan cepat (Quick Entry)
st.subheader("⚡ Pencatatan Cepat")

entry_type = st.radio(
    "Pilih Jenis Transaksi",
    ["Pendapatan", "Pengeluaran"],
    horizontal=True,
    help="Pilih jenis transaksi yang ingin dicatat"
)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if entry_type == "Pendapatan":
        # Load produk
        produk_df = load_data("data/produk.csv")
        deskripsi = st.selectbox("Produk", produk_df['nama'].tolist())
        kategori = "Penjualan"  # Default kategori untuk pendapatan
    else:
        kategori_options = ["Bahan Baku", "Operasional", "Gaji", "Sewa", "Peralatan", "Lainnya"]
        kategori = st.selectbox("Kategori", kategori_options)
        deskripsi = st.text_input("Deskripsi")

with col2:
    jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)

with col3:
    tanggal = st.date_input("Tanggal", datetime.now())
    submit_button = st.button("Simpan")

if submit_button:
    if entry_type == "Pendapatan" and (not deskripsi or jumlah <= 0):
        st.error("Harap isi semua field dengan benar!")
    elif entry_type == "Pengeluaran" and (not deskripsi or not kategori or jumlah <= 0):
        st.error("Harap isi semua field dengan benar!")
    else:
        # Tambahkan data baru
        new_row = pd.DataFrame({
            'tanggal': [tanggal],
            'jenis': [entry_type],
            'kategori': [kategori],
            'deskripsi': [deskripsi],
            'jumlah': [jumlah]
        })
        
        # Gabungkan dengan data yang ada
        updated_df = pd.concat([keuangan_df, new_row], ignore_index=True)
        
        # Simpan ke file
        updated_df.to_csv("data/keuangan.csv", index=False)
        
        st.success(f"{entry_type} berhasil dicatat!")
        st.rerun()

# Tampilkan transaksi terbaru
st.subheader("📋 Transaksi Terbaru")

if not keuangan_df.empty:
    # Urutkan transaksi dari yang terbaru
    sorted_df = keuangan_df.sort_values('tanggal', ascending=False).head(5)
    
    # Format kolom tanggal
    sorted_df['tanggal'] = pd.to_datetime(sorted_df['tanggal']).dt.strftime('%d-%m-%Y')
    
    # Format kolom jumlah ke format Rupiah
    sorted_df['jumlah_fmt'] = sorted_df['jumlah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
    
    # Tambahkan kolom warna untuk jenis transaksi
    sorted_df['color'] = sorted_df['jenis'].apply(
        lambda x: '#e74c3c' if x == 'Pengeluaran' else '#2ecc71'
    )
    
    # Tampilkan transaksi dalam bentuk cards
    for i, row in sorted_df.iterrows():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"**{row['tanggal']}**")
            st.markdown(f"*{row['kategori']}*")
        
        with col2:
            st.markdown(f"**{row['deskripsi']}**")
        
        with col3:
            st.markdown(f"<h4 style='color: {row['color']}'>{row['jumlah_fmt']}</h4>", unsafe_allow_html=True)
        
        st.markdown("---")
else:
    st.info("Belum ada transaksi yang dicatat.")
