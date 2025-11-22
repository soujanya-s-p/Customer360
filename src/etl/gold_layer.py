# src/etl/gold_layer.py
import pandas as pd
import os

os.makedirs("data/gold", exist_ok=True)

print("Loading silver data...")
customers = pd.read_csv("data/silver/customers_clean.csv", low_memory=False)
transactions = pd.read_csv("data/silver/transactions_clean.csv", low_memory=False)
web_logs = pd.read_csv("data/silver/web_logs_clean.csv", low_memory=False)
support = pd.read_csv("data/silver/support_tickets_clean.csv", low_memory=False)
marketing = pd.read_csv("data/silver/marketing_clean.csv", low_memory=False)

print("Building Master Customer Table...")

# MASTER CUSTOMER TABLE (1 row per customer)
master_customers = customers.copy()
master_customers['record_version'] = 1

master_customers.to_csv("data/gold/master_customers.csv", index=False)

print("Saving fact tables...")

# FACT TRANSACTIONS
transactions.to_csv("data/gold/fact_transactions.csv", index=False)

# FACT WEB LOGS
web_logs.to_csv("data/gold/fact_web_logs.csv", index=False)

# FACT SUPPORT TICKETS
support.to_csv("data/gold/fact_support_tickets.csv", index=False)

# FACT MARKETING EVENTS
marketing.to_csv("data/gold/fact_marketing.csv", index=False)

print("Gold layer created successfully ")
