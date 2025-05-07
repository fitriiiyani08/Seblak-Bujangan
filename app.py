import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from utils import load_data, save_data, calculate_profit_loss, get_summary
from sync_data import run_auto_sync, check_pending_sync

# Konfigurasi halaman
st.set_page_config(
    page_title="Seblak Bujangan",
    page_icon="static/images/logo.jpeg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open("static/styles.css", "r", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
if os.path.exists("static/styles.css"):
    load_css()

# Custom HTML untuk header
st.markdown("""
<div class="hero-section fire-bg">
    <div class="floating-pepper" style="top: 10%; left: 10%;">🌶️</div>
    <div class="floating-pepper" style="top: 20%; left: 70%;">🌶️</div>
    <div class="floating-pepper" style="top: 60%; left: 30%;">🔥</div>
    <div class="floating-pepper" style="top: 70%; left: 80%;">🌶️</div>
    <div class="hero-title"><span class="pepper-icon">🌶️</span> Manajemen Keuangan Seblak Bujangan</div>
    <div class="hero-subtitle">Solusi cerdas untuk manajemen keuangan usaha Seblak Anda</div>
    <div style="margin-top: 20px;">
        <span class="spicy-label">Extra Pedas!</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if os.path.exists("static/images/logo.jpeg"):
        st.markdown('<div class="logo-container"><img src="static/images/logo.jpeg" alt="Logo Seblak Bujangan"></div>', unsafe_allow_html=True)
    else:
        st.image("https://img.icons8.com/color/96/000000/noodles.png", width=100)
    
    st.markdown("""
    <div class="sidebar-gradient">
        <div class="floating-pepper" style="top: 10%; right: 10%;">🌶️</div>
        <div class="floating-pepper" style="bottom: 20%; left: 15%;">🔥</div>
        <h2>Seblak Bujangan</h2>
        <p>Aplikasi pencatatan keuangan spesial untuk Seblak Bujangan</p>
        <div class="spicy-label" style="margin-top: 10px; display: inline-block;">Pedas Nendang!</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="fitur-header">Menu Navigasi</div>', unsafe_allow_html=True)
    
# Inisialisasi data
if 'data_initialized' not in st.session_state:
    # Pastikan direktori data ada
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Inisialisasi file keuangan jika belum ada
    if not os.path.exists("data/keuangan.csv"):
        # Membuat contoh data awal untuk demonstrasi
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        keuangan_df = pd.DataFrame({
            'tanggal': [
                today, today, yesterday, yesterday, two_days_ago, two_days_ago
            ],
            'jenis': [
                'Pendapatan', 'Pendapatan', 'Pendapatan', 'Pengeluaran', 'Pendapatan', 'Pengeluaran'
            ],
            'kategori': [
                'Penjualan', 'Penjualan', 'Penjualan', 'Bahan Baku', 'Penjualan', 'Operasional'
            ],
            'deskripsi': [
                'Seblak Original (5 porsi)', 'Seblak Seafood (3 porsi)', 'Seblak Spesial (7 porsi)', 
                'Belanja Bahan', 'Seblak Original (10 porsi)', 'Biaya Listrik'
            ],
            'jumlah': [
                75000, 75000, 140000, 200000, 150000, 50000
            ]
        })
        keuangan_df.to_csv("data/keuangan.csv", index=False)
    
    # Inisialisasi file produk jika belum ada
    if not os.path.exists("data/produk.csv"):
        produk_df = pd.DataFrame({
            'nama': ["Seblak Original", "Seblak Spesial", "Seblak Seafood", "Seblak Tulang", "Mie Instan", "Seblak Ceker", "Seblak Batagor"],
            'harga': [15000, 20000, 25000, 18000, 10000, 22000, 20000]
        })
        produk_df.to_csv("data/produk.csv", index=False)
    
    # Inisialisasi file bahan jika belum ada
    if not os.path.exists("data/bahan.csv"):
        bahan_df = pd.DataFrame({
            'nama': ["Kerupuk", "Mie", "Telur", "Bumbu", "Sayuran", "Bakso", "Sosis", "Seafood", "Ceker", "Batagor"],
            'stok': [10, 20, 30, 5, 3, 15, 15, 10, 8, 12],
            'satuan': ["kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "bungkus"]
        })
        bahan_df.to_csv("data/bahan.csv", index=False)
        
    st.session_state.data_initialized = True

# Jalankan sinkronisasi otomatis ketika aplikasi dimulai
# Ini akan menyinkronkan pesanan dengan data penjualan
run_auto_sync()

# Periksa apakah ada pesanan yang belum disinkronkan
pending_count = check_pending_sync()
if pending_count > 0:
    st.sidebar.warning(f"{pending_count} pesanan menunggu sinkronisasi. Silakan selesaikan di halaman Pesanan.")

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
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="fitur-header"><span class="pepper-icon">🔥</span> Tren Keuangan (7 Hari Terakhir)</div>', unsafe_allow_html=True)

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
st.markdown('<div class="fitur-header">📋 Transaksi Terbaru</div>', unsafe_allow_html=True)

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
        # Custom card styling for each transaction
        card_class = "card-red" if row['jenis'] == 'Pengeluaran' else "card-green"
        jenis_badge = "🔴 Pengeluaran" if row['jenis'] == 'Pengeluaran' else "🟢 Pendapatan"
        
        st.markdown(f"""
        <div class="card {card_class} dashboard-card fade-in">
            <div class="row">
                <div class="col-3">
                    <strong>{row['tanggal']}</strong><br/>
                    <span class="category-pill">{row['kategori']}</span>
                </div>
                <div class="col-6">
                    <strong>{row['deskripsi']}</strong><br/>
                    <small>{jenis_badge}</small>
                </div>
                <div class="col-3" style="text-align: right;">
                    <h3 style="color: {row['color']}; margin: 0;">{row['jumlah_fmt']}</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Belum ada transaksi yang dicatat.")
