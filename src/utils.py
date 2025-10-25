import pandas as pd
from datetime import datetime, timedelta

def load_data():
    """Load all datasets"""
    try:
        users_df = pd.read_csv('data/synthetic_users.csv')
        nps_df = pd.read_csv('data/synthetic_feedback.csv')
        features_df = pd.read_csv('data/synthetic_features.csv')
        return users_df, nps_df, features_df
    except FileNotFoundError:
        return None, None, None

def filter_by_date_range(df, start_date, end_date, date_column='date'):
    """Filter dataframe by date range"""
    df = df.copy()  # Avoid modifying original dataframe
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Convert start_date and end_date to datetime if they're date objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    return df[mask]

def format_number(num):
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(int(num))

def calculate_percent_change(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def get_date_range_presets():
    """Get common date range presets"""
    today = datetime.now()
    return {
        'Last 7 Days': (today - timedelta(days=7), today),
        'Last 30 Days': (today - timedelta(days=30), today),
        'Last 90 Days': (today - timedelta(days=90), today),
        'This Month': (today.replace(day=1), today)
    }