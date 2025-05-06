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
    page_title="Pengeluaran - Seblak Bujangan",
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

# Judul halaman dengan animasi cabai
st.markdown("""
<div class="hero-section spicy-bg">
    <div class="hero-title"><span class="pepper-icon">🔥</span> Pencatatan Pengeluaran</div>
    <div class="hero-subtitle">Kontrol pengeluaran usaha Seblak Bujangan dengan mudah dan terorganisir</div>
</div>
""", unsafe_allow_html=True)

# Load data
keuangan_df = load_data("data/keuangan.csv")

# Form pencatatan pengeluaran
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="fitur-header"><span class="pepper-icon">🔥</span> Catat Pengeluaran Baru</div>', unsafe_allow_html=True)
st.markdown('<div class="form-container spicy-gradient">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    kategori_options = ["Bahan Baku", "Operasional", "Gaji", "Sewa", "Peralatan", "Lainnya"]
    kategori = st.selectbox("Kategori", kategori_options)
    deskripsi = st.text_input("Deskripsi")

with col2:
    jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)

with col3:
    tanggal = st.date_input("Tanggal Pengeluaran", datetime.now())
    
    # Tambahkan tombol untuk menyimpan pengeluaran
    simpan_button = st.button("Simpan Pengeluaran")

if simpan_button:
    if not deskripsi or not kategori or jumlah <= 0:
        st.error("Harap lengkapi semua field pengeluaran!")
    else:
        # Buat data pengeluaran baru
        new_expense = pd.DataFrame({
            'tanggal': [tanggal],
            'jenis': ['Pengeluaran'],
            'kategori': [kategori],
            'deskripsi': [deskripsi],
            'jumlah': [jumlah]
        })
        
        # Tambahkan ke dataframe keuangan
        updated_df = pd.concat([keuangan_df, new_expense], ignore_index=True)
        
        # Simpan ke CSV
        save_data(updated_df, "data/keuangan.csv")
        
        st.success(f"Pengeluaran untuk {deskripsi} berhasil dicatat!")
        
        # Reload data
        keuangan_df = load_data("data/keuangan.csv")

# Tutup form sebelumnya
st.markdown('</div>', unsafe_allow_html=True)

# Tampilkan data pengeluaran
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="fitur-header"><span class="pepper-icon">🌶️</span> Riwayat Pengeluaran</div>', unsafe_allow_html=True)

# Filter untuk data pengeluaran saja
if not keuangan_df.empty:
    pengeluaran_df = keuangan_df[keuangan_df['jenis'] == 'Pengeluaran']
    
    # Opsi filter tanggal
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Dari Tanggal", 
                               datetime.now() - timedelta(days=30),
                               key="pengeluaran_start_date")
    with col2:
        end_date = st.date_input("Sampai Tanggal", 
                             datetime.now(),
                             key="pengeluaran_end_date")
    
    # Filter berdasarkan tanggal
    if not pengeluaran_df.empty:
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        
        filtered_df = pengeluaran_df[(pengeluaran_df['tanggal'] >= start_date) & 
                                   (pengeluaran_df['tanggal'] <= end_date)]
    else:
        filtered_df = pengeluaran_df
    
    # Opsi filter kategori
    if not filtered_df.empty:
        unique_categories = ['Semua'] + sorted(filtered_df['kategori'].unique().tolist())
        selected_category = st.selectbox("Filter berdasarkan Kategori:", unique_categories)
        
        if selected_category != 'Semua':
            filtered_df = filtered_df[filtered_df['kategori'] == selected_category]
    
    # Tampilkan tabel pengeluaran
    if not filtered_df.empty:
        # Konversi tanggal ke format yang lebih mudah dibaca
        display_df = filtered_df.copy()
        display_df['tanggal'] = display_df['tanggal'].dt.strftime('%d-%m-%Y')
        
        # Format kolom jumlah ke format Rupiah
        display_df['jumlah'] = display_df['jumlah'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
        
        # Tampilkan tabel
        st.dataframe(
            display_df[['tanggal', 'kategori', 'deskripsi', 'jumlah']],
            column_config={
                "tanggal": "Tanggal",
                "kategori": "Kategori",
                "deskripsi": "Deskripsi",
                "jumlah": "Jumlah"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Hitung total pengeluaran dalam periode
        total_pengeluaran = filtered_df['jumlah'].sum()
        st.error(f"Total Pengeluaran: Rp {total_pengeluaran:,.0f}".replace(",", "."))
        
        # Visualisasi tren pengeluaran harian
        st.markdown("## 📉 Tren Pengeluaran Harian")
        
        # Agregasi pengeluaran per hari
        daily_expenses = filtered_df.groupby(filtered_df['tanggal'].dt.date)['jumlah'].sum().reset_index()
        daily_expenses.columns = ['tanggal', 'total_pengeluaran']
        
        # Buat line chart
        fig = px.line(
            daily_expenses, 
            x='tanggal', 
            y='total_pengeluaran',
            markers=True,
            title='Tren Pengeluaran Harian',
            color_discrete_sequence=['#e63946']
        )
        
        fig.update_layout(
            xaxis_title='Tanggal',
            yaxis_title='Total Pengeluaran (Rp)',
            hovermode='x unified'
        )
        
        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=8)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Visualisasi pengeluaran berdasarkan kategori
        st.markdown("## 🥧 Distribusi Pengeluaran berdasarkan Kategori")
        
        # Agregasi berdasarkan kategori
        kategori_expenses = filtered_df.groupby('kategori')['jumlah'].sum().reset_index()
        
        # Pie chart untuk kategori pengeluaran
        fig = px.pie(
            kategori_expenses,
            values='jumlah',
            names='kategori',
            title='Distribusi Pengeluaran berdasarkan Kategori',
            color_discrete_sequence=px.colors.sequential.Reds,
            hole=0.4
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart untuk kategori pengeluaran
        fig = px.bar(
            kategori_expenses.sort_values('jumlah', ascending=False),
            x='kategori',
            y='jumlah',
            title='Total Pengeluaran berdasarkan Kategori',
            color='kategori',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        
        fig.update_layout(
            xaxis_title='Kategori',
            yaxis_title='Total Pengeluaran (Rp)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("Tidak ada data pengeluaran dalam rentang tanggal yang dipilih.")
else:
    st.info("Belum ada data pengeluaran yang dicatat.")
