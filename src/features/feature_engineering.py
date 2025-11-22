# src/features/feature_engineering.py
import pandas as pd
import datetime as dt
import os

os.makedirs("data/gold", exist_ok=True)

# Load gold tables
customers = pd.read_csv("data/gold/master_customers.csv")
transactions = pd.read_csv("data/gold/fact_transactions.csv")
web_logs = pd.read_csv("data/gold/fact_web_logs.csv")
support = pd.read_csv("data/gold/fact_support_tickets.csv")
marketing = pd.read_csv("data/gold/fact_marketing.csv")

# Parse date columns
transactions['transaction_date'] = pd.to_datetime(transactions.get('date', transactions.columns[0]), errors='coerce')
web_logs['timestamp'] = pd.to_datetime(web_logs['timestamp'], errors='coerce')
support['ticket_date'] = pd.to_datetime(support.get('date', support.columns[0]), errors='coerce')
marketing['campaign_date'] = pd.to_datetime(marketing.get('campaign_date', marketing.columns[0]), errors='coerce')

# Snapshot for recency
snapshot_date = dt.datetime(2025, 11, 21)

# --- RFM features
rfm = transactions.groupby('customer_id').agg({
    'transaction_date': lambda x: (snapshot_date - x.max()).days,
    'transaction_id': 'count',
    'amount': 'sum'
}).reset_index()
rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# Additional features
rfm['avg_amount'] = rfm['monetary'] / rfm['frequency']
rfm['last_transaction_days'] = rfm['recency']
rfm['total_transactions'] = rfm['frequency']

# --- Web features
web_features = web_logs.groupby('customer_id').agg({
    'session_id': 'count',
    'page_visited': pd.Series.nunique
}).reset_index()
web_features.columns = ['customer_id', 'total_sessions', 'unique_pages']

# --- Support features
support_features = support.groupby('customer_id').agg({
    'ticket_id': 'count',
    'priority': lambda x: (x=='High').sum() if 'priority' in support.columns else 0
}).reset_index()
support_features.columns = ['customer_id', 'total_tickets', 'high_priority_tickets']

# --- Marketing features
marketing_features = marketing.groupby('customer_id').agg({
    'campaign_id': 'count',
    'email_opened': 'sum',
    'clicked_link': 'sum'
}).reset_index()
marketing_features.columns = ['customer_id', 'campaigns_received', 'emails_opened', 'links_clicked']

# Merge all features
features = rfm.merge(web_features, on='customer_id', how='left') \
              .merge(support_features, on='customer_id', how='left') \
              .merge(marketing_features, on='customer_id', how='left')

features.fillna(0, inplace=True)
features.to_csv("data/gold/customer_360_features.csv", index=False)
print("Feature engineering complete ✔️")
