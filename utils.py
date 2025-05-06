import pandas as pd
import os
from datetime import datetime

def load_data(file_path):
    """
    Load data from CSV file and return as pandas DataFrame
    """
    if not os.path.exists(file_path):
        # Return empty DataFrame with correct columns if file doesn't exist
        if 'keuangan.csv' in file_path:
            return pd.DataFrame({
                'tanggal': [],
                'jenis': [],
                'kategori': [],
                'deskripsi': [],
                'jumlah': []
            })
        elif 'produk.csv' in file_path:
            return pd.DataFrame({
                'nama': [],
                'harga': []
            })
        elif 'bahan.csv' in file_path:
            return pd.DataFrame({
                'nama': [],
                'stok': [],
                'satuan': []
            })
        else:
            return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    
    # Convert tanggal to datetime if it exists
    if 'tanggal' in df.columns:
        df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    return df

def save_data(df, file_path):
    """
    Save pandas DataFrame to CSV file
    """
    # Make sure the directory exists
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    df.to_csv(file_path, index=False)
    return True

def calculate_profit_loss(df, start_date=None, end_date=None):
    """
    Calculate profit/loss from financial data
    """
    if df.empty:
        return {
            'pendapatan': 0,
            'pengeluaran': 0,
            'profit_loss': 0
        }
    
    # Convert tanggal to datetime if it's not already
    if not pd.api.types.is_datetime64_dtype(df['tanggal']):
        df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    # Filter by date range if provided
    if start_date and end_date:
        filtered_df = df[(df['tanggal'] >= start_date) & (df['tanggal'] <= end_date)]
    else:
        filtered_df = df
    
    # Calculate total income and expenses
    pendapatan = filtered_df[filtered_df['jenis'] == 'Pendapatan']['jumlah'].sum()
    pengeluaran = filtered_df[filtered_df['jenis'] == 'Pengeluaran']['jumlah'].sum()
    profit_loss = pendapatan - pengeluaran
    
    return {
        'pendapatan': pendapatan,
        'pengeluaran': pengeluaran,
        'profit_loss': profit_loss
    }

def get_summary(df):
    """
    Get summary statistics from financial data
    """
    if df.empty:
        return {
            'pendapatan': 0,
            'pengeluaran': 0,
            'profit_loss': 0,
            'transaksi': 0
        }
    
    # Calculate total income and expenses
    pendapatan = df[df['jenis'] == 'Pendapatan']['jumlah'].sum()
    pengeluaran = df[df['jenis'] == 'Pengeluaran']['jumlah'].sum()
    profit_loss = pendapatan - pengeluaran
    transaksi = len(df)
    
    return {
        'pendapatan': pendapatan,
        'pengeluaran': pengeluaran,
        'profit_loss': profit_loss,
        'transaksi': transaksi
    }

def generate_monthly_report(df, year, month):
    """
    Generate monthly financial report
    """
    if df.empty:
        return {
            'pendapatan': 0,
            'pengeluaran': 0,
            'profit_loss': 0,
            'transaksi': 0,
            'kategori_pendapatan': {},
            'kategori_pengeluaran': {},
            'daily_data': pd.DataFrame()
        }
    
    # Convert tanggal to datetime if it's not already
    if not pd.api.types.is_datetime64_dtype(df['tanggal']):
        df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    # Filter for the specified month
    start_date = pd.Timestamp(year=year, month=month, day=1)
    if month == 12:
        end_date = pd.Timestamp(year=year+1, month=1, day=1) - pd.Timedelta(days=1)
    else:
        end_date = pd.Timestamp(year=year, month=month+1, day=1) - pd.Timedelta(days=1)
    
    monthly_data = df[(df['tanggal'] >= start_date) & (df['tanggal'] <= end_date)]
    
    if monthly_data.empty:
        return {
            'pendapatan': 0,
            'pengeluaran': 0,
            'profit_loss': 0,
            'transaksi': 0,
            'kategori_pendapatan': {},
            'kategori_pengeluaran': {},
            'daily_data': pd.DataFrame()
        }
    
    # Calculate summary metrics
    pendapatan = monthly_data[monthly_data['jenis'] == 'Pendapatan']['jumlah'].sum()
    pengeluaran = monthly_data[monthly_data['jenis'] == 'Pengeluaran']['jumlah'].sum()
    profit_loss = pendapatan - pengeluaran
    transaksi = len(monthly_data)
    
    # Calculate category breakdowns
    pendapatan_by_category = monthly_data[monthly_data['jenis'] == 'Pendapatan'].groupby('kategori')['jumlah'].sum().to_dict()
    pengeluaran_by_category = monthly_data[monthly_data['jenis'] == 'Pengeluaran'].groupby('kategori')['jumlah'].sum().to_dict()
    
    # Daily aggregation
    daily_data = monthly_data.groupby(['tanggal', 'jenis'])['jumlah'].sum().reset_index()
    
    return {
        'pendapatan': pendapatan,
        'pengeluaran': pengeluaran,
        'profit_loss': profit_loss,
        'transaksi': transaksi,
        'kategori_pendapatan': pendapatan_by_category,
        'kategori_pengeluaran': pengeluaran_by_category,
        'daily_data': daily_data
    }
