import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate synthetic user activity data
def generate_user_data():
    """Generate 90 days of synthetic user activity data"""
    
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=x) for x in range(90)]
    
    data = []
    
    for date in dates:
        # Simulate daily active users with weekly seasonality
        day_of_week = date.weekday()
        base_dau = 5000
        
        # Weekend dip
        if day_of_week >= 5:
            base_dau *= 0.7
        
        # Add trend and noise
        days_since_start = (date - start_date).days
        growth_factor = 1 + (days_since_start * 0.005)  # 0.5% daily growth
        dau = int(base_dau * growth_factor * np.random.uniform(0.9, 1.1))
        
        # Calculate other metrics
        mau = int(dau * np.random.uniform(3.5, 4.5))  # MAU is roughly 3.5-4.5x DAU
        new_users = int(dau * np.random.uniform(0.05, 0.15))  # 5-15% are new
        returning_users = dau - new_users
        churned_users = int(mau * np.random.uniform(0.02, 0.05))  # 2-5% churn
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'dau': dau,
            'mau': mau,
            'new_users': new_users,
            'returning_users': returning_users,
            'churned_users': churned_users,
            'sessions': int(dau * np.random.uniform(1.5, 2.5)),  # 1.5-2.5 sessions per user
            'avg_session_duration_min': round(np.random.uniform(8, 15), 2)
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/synthetic_users.csv', index=False)
    print("✅ Generated synthetic_users.csv")
    return df

# Generate synthetic NPS feedback data
def generate_nps_data():
    """Generate synthetic NPS feedback over 90 days"""
    
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=x) for x in range(90)]
    
    data = []
    
    for date in dates:
        # Generate 20-50 NPS responses per day
        num_responses = np.random.randint(20, 50)
        
        for _ in range(num_responses):
            # Simulate NPS distribution (0-10)
            # Skew toward promoters (9-10)
            score = np.random.choice(
                range(11), 
                p=[0.02, 0.02, 0.03, 0.04, 0.05, 0.08, 0.1, 0.15, 0.15, 0.18, 0.18]
            )
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'user_id': f'user_{np.random.randint(1000, 9999)}',
                'nps_score': score,
                'category': 'Promoter' if score >= 9 else ('Passive' if score >= 7 else 'Detractor')
            })
    
    df = pd.DataFrame(data)
    df.to_csv('data/synthetic_feedback.csv', index=False)
    print("✅ Generated synthetic_feedback.csv")
    return df

# Generate feature adoption data
def generate_feature_data():
    """Generate synthetic feature usage data"""
    
    features = [
        'Dark Mode', 'Export Report', 'Advanced Filters', 
        'Mobile App', 'API Integration', 'Collaborative Editing'
    ]
    
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=x) for x in range(90)]
    
    data = []
    
    for date in dates:
        total_users = np.random.randint(4500, 5500)
        
        for feature in features:
            # Different adoption rates for different features
            base_adoption = {
                'Dark Mode': 0.65,
                'Export Report': 0.45,
                'Advanced Filters': 0.30,
                'Mobile App': 0.55,
                'API Integration': 0.15,
                'Collaborative Editing': 0.40
            }
            
            adoption_rate = base_adoption[feature] * np.random.uniform(0.9, 1.1)
            users_adopted = int(total_users * adoption_rate)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'feature': feature,
                'users_adopted': users_adopted,
                'total_users': total_users
            })
    
    df = pd.DataFrame(data)
    df.to_csv('data/synthetic_features.csv', index=False)
    print("✅ Generated synthetic_features.csv")
    return df

if __name__ == "__main__":
    print("🔄 Generating synthetic datasets...")
    generate_user_data()
    generate_nps_data()
    generate_feature_data()
    print("✅ All datasets generated successfully!")
