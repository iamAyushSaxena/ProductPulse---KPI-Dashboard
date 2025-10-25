import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_dau_mau_chart(df):
    """Create DAU vs MAU trend chart"""
    df = df.copy()  # avoid modifying caller's DataFrame / SettingWithCopy
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        raise ValueError("create_dau_mau_chart: 'date' column not found in df")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['dau'],
        mode='lines',
        name='DAU',
        line=dict(color='#3b82f6', width=2),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['mau'],
        mode='lines',
        name='MAU',
        line=dict(color='#8b5cf6', width=2)
    ))
    
    fig.update_layout(
        title='Daily Active Users (DAU) vs Monthly Active Users (MAU)',
        xaxis_title='Date',
        yaxis_title='Number of Users',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_retention_chart(df):
    """Create retention vs churn visualization"""
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate weekly retention
    df['week'] = df['date'].dt.to_period('W')
    weekly = df.groupby('week').agg({
        'returning_users': 'sum',
        'churned_users': 'sum'
    }).reset_index()
    
    weekly['retention_rate'] = (weekly['returning_users'] / 
                                 (weekly['returning_users'] + weekly['churned_users'])) * 100
    weekly['week'] = weekly['week'].astype(str)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekly['week'],
        y=weekly['retention_rate'],
        name='Retention Rate',
        marker_color='#10b981'
    ))
    
    fig.update_layout(
        title='Weekly User Retention Rate (%)',
        xaxis_title='Week',
        yaxis_title='Retention Rate (%)',
        template='plotly_white',
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_nps_distribution(nps_df):
    """Create NPS score distribution"""
    
    distribution = nps_df['category'].value_counts()
    
    colors = {
        'Promoter': '#10b981',
        'Passive': '#f59e0b',
        'Detractor': '#ef4444'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=distribution.index,
        values=distribution.values,
        marker=dict(colors=[colors[cat] for cat in distribution.index]),
        hole=0.4
    )])
    
    fig.update_layout(
        title='NPS Distribution',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_feature_adoption_chart(feature_df):
    """Create feature adoption comparison"""
    
    # Get latest adoption rates
    latest_date = feature_df['date'].max()
    latest = feature_df[feature_df['date'] == latest_date].copy()
    latest['adoption_rate'] = (latest['users_adopted'] / latest['total_users']) * 100
    latest = latest.sort_values('adoption_rate', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=latest['adoption_rate'],
        y=latest['feature'],
        orientation='h',
        marker=dict(color='#6366f1')
    ))
    
    fig.update_layout(
        title='Feature Adoption Rates (%)',
        xaxis_title='Adoption Rate (%)',
        yaxis_title='Feature',
        template='plotly_white',
        height=400,
        xaxis=dict(range=[0, 100])
    )
    
    return fig

def create_growth_trend(df, metric='dau'):
    """Create growth trend with moving average"""
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate 7-day moving average
    df['ma_7'] = df[metric].rolling(window=7).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df[metric],
        mode='lines',
        name='Daily',
        line=dict(color='lightgray', width=1),
        opacity=0.5
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['ma_7'],
        mode='lines',
        name='7-Day Average',
        line=dict(color='#ec4899', width=3)
    ))
    
    fig.update_layout(
        title=f'{metric.upper()} Growth Trend',
        xaxis_title='Date',
        yaxis_title=metric.upper(),
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_session_analysis(df):
    """Create session duration and frequency analysis"""
    df['date'] = pd.to_datetime(df['date'])
    df['sessions_per_user'] = df['sessions'] / df['dau']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['avg_session_duration_min'],
        mode='lines+markers',
        name='Avg Session Duration (min)',
        yaxis='y',
        line=dict(color='#14b8a6')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sessions_per_user'],
        mode='lines+markers',
        name='Sessions per User',
        yaxis='y2',
        line=dict(color='#f97316')
    ))
    
    fig.update_layout(
    title='Session Quality Metrics',
    xaxis_title='Date',
    yaxis=dict(
        title=dict(
            text='Avg Duration (min)',
            font=dict(color='#14b8a6')
        )
    ),
    yaxis2=dict(
        title=dict(
            text='Sessions per User',
            font=dict(color='#f97316')
        ),
        overlaying='y',
        side='right'
    ),
    template='plotly_white',
    height=400,
    hovermode='x unified'
)
    
    return fig