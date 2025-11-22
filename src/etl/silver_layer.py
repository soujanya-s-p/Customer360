# src/etl/silver_layer.py
import pandas as pd
import os

os.makedirs("data/silver", exist_ok=True)

# Load bronze data
customers = pd.read_csv("data/bronze/customers.csv")
transactions = pd.read_csv("data/bronze/transactions.csv")
web_logs = pd.read_csv("data/bronze/web_logs.csv")
support = pd.read_csv("data/bronze/support_tickets.csv")
marketing = pd.read_csv("data/bronze/marketing.csv")

# ---- Clean Customers ----
customers['email'] = customers['email'].fillna('unknown@example.com')
customers['phone'] = customers['phone'].astype(str).str.replace('-', '').str.strip()
customers_clean = customers.drop_duplicates(subset=['email', 'phone'])
customers_clean.to_csv("data/silver/customers_clean.csv", index=False)

# ---- Clean Transactions ----
transactions['amount'] = transactions['amount'].apply(lambda x: max(0, x))  # remove negative
transactions.to_csv("data/silver/transactions_clean.csv", index=False)

# ---- Clean Logs ----
web_logs.to_csv("data/silver/web_logs_clean.csv", index=False)

# ---- Clean Support ----
support.to_csv("data/silver/support_tickets_clean.csv", index=False)

# ---- Clean Marketing ----
marketing.to_csv("data/silver/marketing_clean.csv", index=False)

print("Silver layer cleaning complete.")
