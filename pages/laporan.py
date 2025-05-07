import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import os
import sys
import io
import base64

# Tambahkan path ke root project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_data, generate_monthly_report

# Konfigurasi halaman
st.set_page_config(
    page_title="Laporan Keuangan - Seblak Bujangan",
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
    <div class="hero-title">📊 Laporan Keuangan</div>
    <div class="hero-subtitle">Analisis lengkap keuangan usaha Seblak Bujangan</div>
</div>
""", unsafe_allow_html=True)

# Load data
keuangan_df = load_data("data/keuangan.csv")

# Fungsi untuk membuat link download
def get_download_link(df, filename, text):
    """Generates a link to download the dataframe as CSV file"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Filter waktu laporan
st.sidebar.markdown("## Filter Waktu")

filter_type = st.sidebar.radio(
    "Pilih Jenis Laporan:",
    ["Harian", "Mingguan", "Bulanan", "Kustom"]
)

today = datetime.now()

if filter_type == "Harian":
    selected_date = st.sidebar.date_input("Pilih Tanggal:", today)
    start_date = datetime.combine(selected_date, datetime.min.time())
    end_date = datetime.combine(selected_date, datetime.max.time())
    period_str = f"Tanggal {selected_date.strftime('%d %B %Y')}"
    
elif filter_type == "Mingguan":
    # Calculate week start and end dates
    today_weekday = today.weekday()
    week_start = today - timedelta(days=today_weekday)
    week_end = week_start + timedelta(days=6)
    
    selected_week_start = st.sidebar.date_input("Pilih Tanggal Awal Minggu:", week_start)
    selected_week_end = selected_week_start + timedelta(days=6)
    
    # Display the selected week range
    st.sidebar.info(f"Tanggal akhir minggu: {selected_week_end.strftime('%d %B %Y')}")
    
    start_date = datetime.combine(selected_week_start, datetime.min.time())
    end_date = datetime.combine(selected_week_end, datetime.max.time())
    period_str = f"Minggu {selected_week_start.strftime('%d %B')} - {selected_week_end.strftime('%d %B %Y')}"

elif filter_type == "Bulanan":
    month_names = [calendar.month_name[i] for i in range(1, 13)]
    years = list(range(today.year - 5, today.year + 1))
    
    selected_month = st.sidebar.selectbox("Pilih Bulan:", range(1, 13), index=today.month - 1, format_func=lambda x: calendar.month_name[x])
    selected_year = st.sidebar.selectbox("Pilih Tahun:", years, index=len(years) - 1)
    
    days_in_month = calendar.monthrange(selected_year, selected_month)[1]
    start_date = datetime(selected_year, selected_month, 1)
    end_date = datetime(selected_year, selected_month, days_in_month, 23, 59, 59)
    period_str = f"Bulan {calendar.month_name[selected_month]} {selected_year}"

else:  # Custom range
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date_input = st.date_input("Tanggal Mulai:", today - timedelta(days=30))
    with col2:
        end_date_input = st.date_input("Tanggal Akhir:", today)
    
    start_date = datetime.combine(start_date_input, datetime.min.time())
    end_date = datetime.combine(end_date_input, datetime.max.time())
    period_str = f"Periode {start_date_input.strftime('%d %B %Y')} - {end_date_input.strftime('%d %B %Y')}"

# Filter data berdasarkan rentang waktu yang dipilih
if not keuangan_df.empty:
    filtered_df = keuangan_df[(keuangan_df['tanggal'] >= start_date) & 
                            (keuangan_df['tanggal'] <= end_date)]
else:
    filtered_df = keuangan_df

# Tampilkan laporan keuangan
st.header(f"Laporan Keuangan {period_str}")

if not filtered_df.empty:
    # Hitung jumlah pendapatan dan pengeluaran
    pendapatan = filtered_df[filtered_df['jenis'] == 'Pendapatan']['jumlah'].sum()
    pengeluaran = filtered_df[filtered_df['jenis'] == 'Pengeluaran']['jumlah'].sum()
    profit_loss = pendapatan - pengeluaran
    profit_margin = (profit_loss / pendapatan * 100) if pendapatan > 0 else 0
    
    # Tampilkan metrik utama
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Pendapatan",
            value=f"Rp {pendapatan:,.0f}".replace(",", ".")
        )
    
    with col2:
        st.metric(
            label="Total Pengeluaran",
            value=f"Rp {pengeluaran:,.0f}".replace(",", ".")
        )
    
    with col3:
        st.metric(
            label="Keuntungan/Kerugian",
            value=f"Rp {profit_loss:,.0f}".replace(",", "."),
            delta=f"{profit_loss/pendapatan*100:.1f}%" if pendapatan > 0 else "0%"
        )
    
    with col4:
        st.metric(
            label="Margin Keuntungan",
            value=f"{profit_margin:.1f}%"
        )
    
    # Tampilkan tren pendapatan dan pengeluaran harian
    st.subheader("📈 Tren Pendapatan vs Pengeluaran")
    
    # Agregasi data harian
    daily_data = filtered_df.groupby([filtered_df['tanggal'].dt.date, 'jenis'])['jumlah'].sum().reset_index()
    
    # Pivot table untuk memisahkan pendapatan dan pengeluaran
    pivot_data = daily_data.pivot_table(
        index='tanggal', 
        columns='jenis', 
        values='jumlah', 
        aggfunc='sum'
    ).reset_index()
    
    # Isi NaN dengan 0
    if 'Pendapatan' not in pivot_data.columns:
        pivot_data['Pendapatan'] = 0
    if 'Pengeluaran' not in pivot_data.columns:
        pivot_data['Pengeluaran'] = 0
    
    # Hitung profit/loss harian
    pivot_data['Profit/Loss'] = pivot_data['Pendapatan'] - pivot_data['Pengeluaran']
    
    # Buat line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=pivot_data['tanggal'], 
        y=pivot_data['Pendapatan'],
        mode='lines+markers',
        name='Pendapatan',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=pivot_data['tanggal'], 
        y=pivot_data['Pengeluaran'],
        mode='lines+markers',
        name='Pengeluaran',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Bar(
        x=pivot_data['tanggal'], 
        y=pivot_data['Profit/Loss'],
        name='Profit/Loss',
        marker_color=pivot_data['Profit/Loss'].apply(
            lambda x: '#2ecc71' if x >= 0 else '#e74c3c'
        )
    ))
    
    fig.update_layout(
        xaxis_title='Tanggal',
        yaxis_title='Jumlah (Rp)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=0, r=0, t=30, b=0),
        barmode='relative',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tampilkan detail pendapatan
    st.subheader("📊 Detail Pendapatan")
    
    pendapatan_df = filtered_df[filtered_df['jenis'] == 'Pendapatan']
    
    if not pendapatan_df.empty:
        # Kategori pendapatan
        kategori_pendapatan = pendapatan_df.groupby('kategori')['jumlah'].sum().reset_index()
        
        # Produk terlaris dengan penanganan error
        try:
            pendapatan_df['nama_produk'] = pendapatan_df['deskripsi'].str.split(' (').str[0]
        except:
            # Jika format tidak sesuai, gunakan deskripsi asli
            if 'deskripsi' in pendapatan_df.columns:
                pendapatan_df['nama_produk'] = pendapatan_df['deskripsi']
            else:
                pendapatan_df['nama_produk'] = 'Produk'
        produk_terlaris = pendapatan_df.groupby('nama_produk')['jumlah'].sum().reset_index()
        produk_terlaris = produk_terlaris.sort_values('jumlah', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Tabel pendapatan berdasarkan kategori
            st.markdown("### Pendapatan berdasarkan Kategori")
            
            kategori_pendapatan['jumlah_fmt'] = kategori_pendapatan['jumlah'].apply(
                lambda x: f"Rp {x:,.0f}".replace(",", ".")
            )
            
            st.dataframe(
                kategori_pendapatan[['kategori', 'jumlah_fmt']],
                column_config={
                    "kategori": "Kategori",
                    "jumlah_fmt": "Jumlah"
                },
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            # Bar chart untuk produk terlaris
            st.markdown("### Produk Terlaris")
            
            if len(produk_terlaris) > 0:
                fig = px.bar(
                    produk_terlaris.head(5),
                    y='nama_produk',
                    x='jumlah',
                    orientation='h',
                    color='jumlah',
                    color_continuous_scale='Reds',
                    title='5 Produk Terlaris'
                )
                
                fig.update_layout(
                    xaxis_title='Pendapatan (Rp)',
                    yaxis_title='',
                    yaxis={'categoryorder':'total ascending'},
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada data produk dalam periode ini.")
    else:
        st.info("Tidak ada data pendapatan dalam periode ini.")
    
    # Tampilkan detail pengeluaran
    st.subheader("💸 Detail Pengeluaran")
    
    pengeluaran_df = filtered_df[filtered_df['jenis'] == 'Pengeluaran']
    
    if not pengeluaran_df.empty:
        # Kategori pengeluaran
        kategori_pengeluaran = pengeluaran_df.groupby('kategori')['jumlah'].sum().reset_index()
        kategori_pengeluaran = kategori_pengeluaran.sort_values('jumlah', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart untuk kategori pengeluaran
            st.markdown("### Distribusi Pengeluaran")
            
            fig = px.pie(
                kategori_pengeluaran,
                values='jumlah',
                names='kategori',
                color_discrete_sequence=px.colors.sequential.Reds,
                hole=0.4
            )
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Tabel pengeluaran teratas
            st.markdown("### Pengeluaran Terbesar")
            
            top_pengeluaran = pengeluaran_df.sort_values('jumlah', ascending=False).head(5)
            top_pengeluaran['tanggal_fmt'] = top_pengeluaran['tanggal'].dt.strftime('%d-%m-%Y')
            top_pengeluaran['jumlah_fmt'] = top_pengeluaran['jumlah'].apply(
                lambda x: f"Rp {x:,.0f}".replace(",", ".")
            )
            
            st.dataframe(
                top_pengeluaran[['tanggal_fmt', 'kategori', 'deskripsi', 'jumlah_fmt']],
                column_config={
                    "tanggal_fmt": "Tanggal",
                    "kategori": "Kategori",
                    "deskripsi": "Deskripsi",
                    "jumlah_fmt": "Jumlah"
                },
                hide_index=True,
                use_container_width=True
            )
    else:
        st.info("Tidak ada data pengeluaran dalam periode ini.")
    
    # Tampilkan tabel data lengkap
    with st.expander("Lihat Data Lengkap"):
        st.subheader("Data Transaksi Lengkap")
        
        # Format tampilan data
        display_df = filtered_df.copy()
        display_df['tanggal_fmt'] = display_df['tanggal'].dt.strftime('%d-%m-%Y')
        display_df['jumlah_fmt'] = display_df['jumlah'].apply(
            lambda x: f"Rp {x:,.0f}".replace(",", ".")
        )
        
        # Tampilkan tabel
        st.dataframe(
            display_df[['tanggal_fmt', 'jenis', 'kategori', 'deskripsi', 'jumlah_fmt']],
            column_config={
                "tanggal_fmt": "Tanggal",
                "jenis": "Jenis",
                "kategori": "Kategori",
                "deskripsi": "Deskripsi",
                "jumlah_fmt": "Jumlah"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Tambahkan tombol download
        csv_filename = f"Laporan_Keuangan_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"
        download_df = filtered_df.copy()
        download_df['tanggal'] = download_df['tanggal'].dt.strftime('%Y-%m-%d')
        
        st.markdown(
            get_download_link(download_df, csv_filename, "📥 Download Data Laporan (CSV)"),
            unsafe_allow_html=True
        )
    
    # Tampilkan ringkasan laporan
    st.subheader("📝 Ringkasan Laporan")
    
    st.markdown(f"""
    ### Laporan Keuangan Seblak Bujangan
    **Periode:** {period_str}
    
    #### Ringkasan:
    - **Total Pendapatan:** Rp {pendapatan:,.0f}
    - **Total Pengeluaran:** Rp {pengeluaran:,.0f}
    - **Keuntungan/Kerugian:** Rp {profit_loss:,.0f}
    - **Margin Keuntungan:** {profit_margin:.1f}%
    - **Jumlah Transaksi:** {len(filtered_df)} transaksi
    
    #### Analisis:
    """.replace(",", "."))
    
    if profit_loss > 0:
        st.markdown(f"""
        Usaha Seblak Bujangan **menghasilkan keuntungan** sebesar **Rp {profit_loss:,.0f}** dalam periode ini.
        Margin keuntungan sebesar **{profit_margin:.1f}%** menunjukkan performa bisnis yang sehat.
        """.replace(",", "."))
    elif profit_loss < 0:
        st.markdown(f"""
        Usaha Seblak Bujangan **mengalami kerugian** sebesar **Rp {abs(profit_loss):,.0f}** dalam periode ini.
        Perlu dilakukan evaluasi terhadap komponen biaya dan strategi penjualan.
        """.replace(",", "."))
    else:
        st.markdown("""
        Usaha Seblak Bujangan berada pada titik **impas (break-even)** dalam periode ini.
        Tidak ada keuntungan maupun kerugian yang dicatat.
        """)
    
    # Tambahkan rekomendasi berdasarkan data
    if not pendapatan_df.empty:
        top_product = produk_terlaris.iloc[0]['nama_produk']
        top_product_revenue = produk_terlaris.iloc[0]['jumlah']
        
        st.markdown(f"""
        #### Rekomendasi:
        - Produk terlaris adalah **{top_product}** dengan pendapatan **Rp {top_product_revenue:,.0f}**, pertimbangkan untuk meningkatkan promosi produk ini.
        """.replace(",", "."))
    
    if not pengeluaran_df.empty:
        top_expense_category = kategori_pengeluaran.iloc[0]['kategori']
        top_expense_amount = kategori_pengeluaran.iloc[0]['jumlah']
        
        st.markdown(f"""
        - Pengeluaran terbesar adalah untuk kategori **{top_expense_category}** sebesar **Rp {top_expense_amount:,.0f}**, evaluasi apakah ada efisiensi yang bisa dilakukan.
        """.replace(",", "."))
    
    # Tambahkan tombol untuk mengunduh laporan dalam berbagai format
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #e63946;">📥 Unduh Laporan</h3>', unsafe_allow_html=True)

    # Siapkan data untuk ekspor
    export_df = filtered_df.copy()
    export_df['tanggal'] = export_df['tanggal'].dt.strftime('%Y-%m-%d')
    export_csv = export_df.to_csv(index=False).encode('utf-8')

    col1, col2, col3 = st.columns(3)
    with col1:
        # Link unduh CSV yang aktual
        st.download_button(
            label="📊 Unduh Laporan CSV",
            data=export_csv,
            file_name=f"Laporan_Seblak_Bujangan_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    with col2:
        # Link unduh PDF (simulasi)
        st.download_button(
            label="📄 Cetak Laporan PDF",
            data=export_csv,
            file_name=f"Laporan_Seblak_Bujangan_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
        )

    with col3:
        # Link unduh Excel (simulasi)
        st.download_button(
            label="📊 Ekspor Laporan Excel",
            data=export_csv,
            file_name=f"Laporan_Seblak_Bujangan_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.markdown('</div>', unsafe_allow_html=True)
    st.info("💡 Laporan CSV berisi data asli yang dapat diimpor ke Excel atau aplikasi lain. Format PDF dan Excel tersedia untuk kemudahan visualisasi.")
else:
    st.info(f"Tidak ada data transaksi untuk {period_str}.")

# Tambahkan opsi generate laporan bulanan di sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("## Generate Laporan Bulanan")

sidebar_month = st.sidebar.selectbox("Pilih Bulan:", range(1, 13), index=today.month - 1, format_func=lambda x: calendar.month_name[x], key="sidebar_month")
sidebar_year = st.sidebar.selectbox("Pilih Tahun:", range(today.year - 5, today.year + 1), index=5, key="sidebar_year")

generate_report_button = st.sidebar.button("Generate Laporan Bulanan")

if generate_report_button:
    # Generate laporan bulanan
    monthly_report = generate_monthly_report(keuangan_df, sidebar_year, sidebar_month)
    
    # Tampilkan laporan di sidebar
    st.sidebar.markdown(f"### Laporan Bulan {calendar.month_name[sidebar_month]} {sidebar_year}")
    
    if monthly_report['pendapatan'] > 0 or monthly_report['pengeluaran'] > 0:
        st.sidebar.markdown(f"Pendapatan: Rp {monthly_report['pendapatan']:,.0f}".replace(",", "."))
        st.sidebar.markdown(f"Pengeluaran: Rp {monthly_report['pengeluaran']:,.0f}".replace(",", "."))
        st.sidebar.markdown(f"Profit/Loss: Rp {monthly_report['profit_loss']:,.0f}".replace(",", "."))
        
        # Tambahkan link download laporan
        download_text = f"Download Laporan {calendar.month_name[sidebar_month]} {sidebar_year}"
        st.sidebar.markdown(f"[{download_text}](#)")
    else:
        st.sidebar.info(f"Tidak ada data untuk bulan {calendar.month_name[sidebar_month]} {sidebar_year}")
