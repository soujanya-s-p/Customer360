# src/dashboard/app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---- Page Config ----
st.set_page_config(page_title="Enterprise Customer 360° Dashboard", layout="wide")
st.title("Enterprise Customer 360° Dashboard")

# ---- Load Data ----
df = pd.read_csv("data/gold/customer_360_features.csv")

# ---- Generate churn probability if missing ----
if 'churn_prob' not in df.columns:
    df['churn_prob'] = np.clip(df['recency'] / df['recency'].max() + np.random.rand(len(df))*0.1, 0, 1)

# ---- Segment Classification ----
df['segment'] = np.where((df['frequency'] > df['frequency'].mean()) & (df['monetary'] > df['monetary'].mean()), 'VIP',
                         np.where(df['churn_prob'] > 0.7, 'At-Risk', 'Normal'))

# ---- Sidebar Filters ----
st.sidebar.header("Filters")
churn_range = st.sidebar.slider("Churn Probability", 0.0, 1.0, (0.0, 1.0))
freq_range = st.sidebar.slider("Frequency Range", int(df['frequency'].min()), int(df['frequency'].max()), 
                               (int(df['frequency'].min()), int(df['frequency'].max())))
monetary_range = st.sidebar.slider("Monetary Range", float(df['monetary'].min()), float(df['monetary'].max()), 
                                   (float(df['monetary'].min()), float(df['monetary'].max())))

filtered_df = df[(df['churn_prob'] >= churn_range[0]) & (df['churn_prob'] <= churn_range[1]) &
                 (df['frequency'] >= freq_range[0]) & (df['frequency'] <= freq_range[1]) &
                 (df['monetary'] >= monetary_range[0]) & (df['monetary'] <= monetary_range[1])]

# ---- KPI Cards ----
st.header("Customer Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", filtered_df['customer_id'].nunique())
col2.metric("Average Monetary Value", f"${filtered_df['monetary'].mean():.2f}")
col3.metric("Average Transaction Amount", f"${filtered_df['avg_amount'].mean():.2f}")
col4.metric("Average Sessions per Customer", f"{filtered_df['total_sessions'].mean():.1f}")

# ---- Top 10 Customers (At-Risk vs VIP) ----
st.header("Top Customers")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 At-Risk Customers")
    top_at_risk = filtered_df[filtered_df['segment']=='At-Risk'].sort_values('churn_prob', ascending=False).head(10)
    st.dataframe(top_at_risk[['customer_id','recency','frequency','monetary','churn_prob','segment']].style.applymap(
        lambda val: 'background-color: #e74c3c' if val=='At-Risk' else '', subset=['segment']
    ))

with col2:
    st.subheader("Top 10 VIP Customers")
    top_vip = filtered_df[filtered_df['segment']=='VIP'].sort_values('monetary', ascending=False).head(10)
    st.dataframe(top_vip[['customer_id','recency','frequency','monetary','churn_prob','segment']].style.applymap(
        lambda val: 'background-color: #2ecc71' if val=='VIP' else '', subset=['segment']
    ))

# ---- Transactions Distribution (Interactive) ----
st.header("Transactions Distribution")
fig_trans = px.histogram(filtered_df, x='total_transactions', nbins=20, color='segment',
                         title='Transactions Distribution by Customer Segment', hover_data=['customer_id'])
st.plotly_chart(fig_trans, use_container_width=True)

# ---- Customer Engagement (Stacked Bar) ----
st.header("Customer Engagement Overview")
engagement_cols = ['total_sessions','unique_pages','total_tickets','high_priority_tickets']
engagement_df = filtered_df[engagement_cols].sum().reset_index()
engagement_df.columns = ['Metric','Total']
fig_eng = px.bar(engagement_df, x='Metric', y='Total', color='Metric', text='Total', title='Customer Engagement Metrics')
st.plotly_chart(fig_eng, use_container_width=True)

# ---- Campaign Performance (Grouped Bar) ----
st.header("Campaign Engagement")
campaign_cols = ['campaigns_received','emails_opened','links_clicked']
campaign_df = filtered_df[campaign_cols].sum().reset_index()
campaign_df.columns = ['Metric','Total']
fig_campaign = px.bar(campaign_df, x='Metric', y='Total', color='Metric', text='Total', title='Campaign Engagement Metrics')
st.plotly_chart(fig_campaign, use_container_width=True)

# ---- Churn Probability Distribution ----
st.header("Churn Probability Distribution")
fig_churn = px.histogram(filtered_df, x='churn_prob', nbins=10, color='segment',
                         title='Churn Probability Distribution', hover_data=['customer_id'])
st.plotly_chart(fig_churn, use_container_width=True)

# ---- Customer Segments Pie Chart ----
st.header("Customer Segments Distribution")
segment_counts = filtered_df['segment'].value_counts().reset_index()
segment_counts.columns = ['Segment','Count']
fig_pie = px.pie(segment_counts, names='Segment', values='Count', color='Segment',
                 color_discrete_map={'VIP':'#2ecc71','At-Risk':'#e74c3c','Normal':'#f1c40f'},
                 title="Customer Segments")
st.plotly_chart(fig_pie, use_container_width=True)
