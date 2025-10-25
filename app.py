import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.metrics import (
    calculate_retention_rate, calculate_churn_rate, calculate_nps,
    calculate_dau_mau_ratio, calculate_feature_adoption, 
    calculate_growth_rate, get_summary_stats
)
from src.visualizations import (
    create_dau_mau_chart, create_retention_chart, create_nps_distribution,
    create_feature_adoption_chart, create_growth_trend, create_session_analysis
)
from src.utils import load_data, filter_by_date_range, format_number

# Page configuration
st.set_page_config(
    page_title="ProductPulse - KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - STRONG OVERRIDE
st.markdown("""
    <style>
    /* Force everything to light mode colors */
    * {
        color: inherit;
    }
    
    /* Metric label - FORCE VISIBLE */
    div[data-testid="stMetricLabel"] > div,
    div[data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #555555 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Metric value - FORCE VISIBLE */
    div[data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #111111 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Metric delta - FORCE VISIBLE */
    div[data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        color: #666666 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Metric container */
    .stMetric {
        background-color: white !important;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 ProductPulse - Product KPI Dashboard")
st.markdown("**Real-time product analytics for data-driven decisions**")
st.markdown("---")

# Load data
users_df, nps_df, features_df = load_data()

if users_df is None:
    st.error("⚠️ Data files not found! Please run `python data/generate_data.py` first.")
    st.stop()

# Sidebar filters
st.sidebar.header("⚙️ Filters")

# Date range selector
date_range = st.sidebar.selectbox(
    "Select Date Range",
    ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"]
)

today = datetime.now()

if date_range == "Last 7 Days":
    start_date = today - timedelta(days=7)
    end_date = today
elif date_range == "Last 30 Days":
    start_date = today - timedelta(days=30)
    end_date = today
elif date_range == "Last 90 Days":
    start_date = today - timedelta(days=90)
    end_date = today
else:
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start Date", today - timedelta(days=30))
    end_date = col2.date_input("End Date", today)

# Filter data
filtered_users = filter_by_date_range(users_df, start_date, end_date)
filtered_nps = filter_by_date_range(nps_df, start_date, end_date)
filtered_features = filter_by_date_range(features_df, start_date, end_date)

# Calculate metrics
stats = get_summary_stats(filtered_users)
retention = calculate_retention_rate(filtered_users)
churn = calculate_churn_rate(filtered_users)
nps_score = calculate_nps(filtered_nps)
stickiness = calculate_dau_mau_ratio(filtered_users)
growth = calculate_growth_rate(filtered_users, 'dau', 30)

# Key Metrics Row
st.subheader("🎯 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Current DAU",
        value=format_number(stats['current_dau']),
        delta=f"{growth}% growth"
    )

with col2:
    st.metric(
        label="Current MAU",
        value=format_number(stats['current_mau']),
        delta=None
    )

with col3:
    st.metric(
        label="Retention Rate",
        value=f"{retention}%",
        delta=f"{retention - 85:.1f}%" if retention > 85 else f"{retention - 85:.1f}%",
        delta_color="normal" if retention > 85 else "inverse"
    )

with col4:
    st.metric(
        label="Net Promoter Score",
        value=f"{nps_score}",
        delta="Excellent" if nps_score > 50 else ("Good" if nps_score > 30 else "Needs Improvement"),
        delta_color="off"
    )

st.markdown("---")

# Second Row Metrics
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        label="Churn Rate",
        value=f"{churn}%",
        delta=f"{churn - 3:.1f}%" if churn > 3 else f"{churn - 3:.1f}%",
        delta_color="inverse"
    )

with col6:
    st.metric(
        label="Stickiness (DAU/MAU)",
        value=f"{stickiness}%",
        delta="Healthy" if stickiness > 20 else "Monitor",
        delta_color="off"
    )

with col7:
    st.metric(
        label="Avg Session Duration",
        value=f"{stats['avg_session_duration']} min",
        delta=None
    )

with col8:
    st.metric(
        label="Total Sessions Today",
        value=format_number(stats['total_sessions_today']),
        delta=None
    )

st.markdown("---")

# Charts Section
st.subheader("📈 Trend Analysis")

# Row 1: DAU/MAU and Retention
col1, col2 = st.columns(2)

with col1:
    fig_dau_mau = create_dau_mau_chart(filtered_users)
    st.plotly_chart(fig_dau_mau, use_container_width=True)

with col2:
    fig_retention = create_retention_chart(filtered_users)
    st.plotly_chart(fig_retention, use_container_width=True)

# Row 2: NPS and Feature Adoption
col3, col4 = st.columns(2)

with col3:
    fig_nps = create_nps_distribution(filtered_nps)
    st.plotly_chart(fig_nps, use_container_width=True)

with col4:
    fig_features = create_feature_adoption_chart(filtered_features)
    st.plotly_chart(fig_features, use_container_width=True)

# Row 3: Growth Trend and Session Analysis
st.markdown("---")
st.subheader("🚀 Growth & Engagement Metrics")

col5, col6 = st.columns(2)

with col5:
    fig_growth = create_growth_trend(filtered_users, 'dau')
    st.plotly_chart(fig_growth, use_container_width=True)

with col6:
    fig_sessions = create_session_analysis(filtered_users)
    st.plotly_chart(fig_sessions, use_container_width=True)

# Data Table Section
st.markdown("---")
st.subheader("📋 Raw Data Explorer")

data_view = st.selectbox(
    "Select Data to View",
    ["User Activity", "NPS Feedback", "Feature Adoption"]
)

if data_view == "User Activity":
    st.dataframe(filtered_users.tail(20), use_container_width=True)
    
    # Download button
    csv = filtered_users.to_csv(index=False)
    st.download_button(
        label="📥 Download User Data (CSV)",
        data=csv,
        file_name="user_activity_data.csv",
        mime="text/csv"
    )

elif data_view == "NPS Feedback":
    st.dataframe(filtered_nps.tail(50), use_container_width=True)
    
    csv = filtered_nps.to_csv(index=False)
    st.download_button(
        label="📥 Download NPS Data (CSV)",
        data=csv,
        file_name="nps_feedback_data.csv",
        mime="text/csv"
    )

else:
    st.dataframe(filtered_features.tail(20), use_container_width=True)
    
    csv = filtered_features.to_csv(index=False)
    st.download_button(
        label="📥 Download Feature Data (CSV)",
        data=csv,
        file_name="feature_adoption_data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 20px;'>
        <p>📊<strong>ProductPulse</strong> - Interactive KPI Dashboard for PMs</p>
        <p>Built with Streamlit & Python <strong>| Last Updated:</strong> {}</p>
        <p>© 2025 <strong>Ayush Saxena</strong>. All rights reserved.</p>
    </div>
""".format(datetime.now().strftime("%d-%b-%Y At %I:%M %p")), unsafe_allow_html=True)

# Sidebar Info
st.sidebar.markdown("---")
st.sidebar.info("""
    **💡 Quick Tips:**
    - Use date filters to analyze specific periods
    - DAU/MAU ratio > 20% indicates good stickiness
    - NPS > 50 is excellent, 30-50 is good
    - Monitor retention rate weekly
    - Track feature adoption for launch success
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
    **📚 About Metrics:**
    - **DAU**: Daily Active Users
    - **MAU**: Monthly Active Users  
    - **Retention**: % of users returning
    - **Churn**: % of users leaving
    - **NPS**: Net Promoter Score (-100 to +100)
    - **Stickiness**: DAU/MAU ratio
""")