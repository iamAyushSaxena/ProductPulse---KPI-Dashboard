import pandas as pd
import numpy as np

def calculate_retention_rate(df, period_days=30):
    """
    Calculate user retention rate
    Returns percentage of users who return after first visit
    """
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Simple retention calculation: returning_users / (returning_users + churned_users)
    recent_data = df.tail(period_days)
    total_returning = recent_data['returning_users'].sum()
    total_churned = recent_data['churned_users'].sum()
    
    if total_returning + total_churned == 0:
        return 0
    
    retention_rate = (total_returning / (total_returning + total_churned)) * 100
    return round(retention_rate, 2)

def calculate_churn_rate(df, period_days=30):
    """
    Calculate churn rate over specified period
    """
    df['date'] = pd.to_datetime(df['date'])
    recent_data = df.tail(period_days)
    
    avg_mau = recent_data['mau'].mean()
    total_churned = recent_data['churned_users'].sum()
    
    if avg_mau == 0:
        return 0
    
    churn_rate = (total_churned / (avg_mau * period_days)) * 100
    return round(churn_rate, 2)

def calculate_nps(nps_df):
    """
    Calculate Net Promoter Score
    NPS = % Promoters - % Detractors
    """
    if len(nps_df) == 0:
        return 0
    
    total = len(nps_df)
    promoters = len(nps_df[nps_df['category'] == 'Promoter'])
    detractors = len(nps_df[nps_df['category'] == 'Detractor'])
    
    nps = ((promoters - detractors) / total) * 100
    return round(nps, 1)

def calculate_dau_mau_ratio(df, period_days=30):
    """
    Calculate DAU/MAU ratio (stickiness metric)
    """
    recent_data = df.tail(period_days)
    avg_dau = recent_data['dau'].mean()
    avg_mau = recent_data['mau'].mean()
    
    if avg_mau == 0:
        return 0
    
    ratio = (avg_dau / avg_mau) * 100
    return round(ratio, 2)

def calculate_feature_adoption(feature_df, feature_name=None):
    """
    Calculate adoption rate for features
    """
    if feature_name:
        feature_df = feature_df[feature_df['feature'] == feature_name]
    
    recent_data = feature_df.tail(30)
    avg_adopted = recent_data['users_adopted'].mean()
    avg_total = recent_data['total_users'].mean()
    
    if avg_total == 0:
        return 0
    
    adoption_rate = (avg_adopted / avg_total) * 100
    return round(adoption_rate, 2)

def calculate_growth_rate(df, metric='dau', period_days=30):
    """
    Calculate growth rate for a metric over period
    """
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    if len(df) < period_days:
        return 0
    
    recent = df.tail(period_days)
    previous = df.tail(period_days * 2).head(period_days)
    
    recent_avg = recent[metric].mean()
    previous_avg = previous[metric].mean()
    
    if previous_avg == 0:
        return 0
    
    growth = ((recent_avg - previous_avg) / previous_avg) * 100
    return round(growth, 2)

def get_summary_stats(df):
    """
    Get summary statistics for dashboard
    """
    df['date'] = pd.to_datetime(df['date'])
    latest = df.iloc[-1]
    
    stats = {
        'current_dau': int(latest['dau']),
        'current_mau': int(latest['mau']),
        'avg_session_duration': round(df.tail(7)['avg_session_duration_min'].mean(), 1),
        'total_sessions_today': int(latest['sessions'])
    }
    
    return stats
