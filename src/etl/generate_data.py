# src/etl/generate_data.py
import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker()

os.makedirs("data/bronze", exist_ok=True)

# ---- Customers ----
num_customers = 10000
customers = []

for i in range(num_customers):
    customers.append({
        "customer_id": i+1,
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "signup_date": fake.date_between(start_date='-3y', end_date='today')
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv("data/bronze/customers.csv", index=False)

# ---- Transactions ----
num_transactions = 100000
transactions = []

for i in range(num_transactions):
    cust_id = random.randint(1, num_customers)
    transactions.append({
        "transaction_id": i+1,
        "customer_id": cust_id,
        "amount": round(random.uniform(10, 1000), 2),
        "category": random.choice(['Electronics','Fashion','Home','Sports','Books']),
        "date": fake.date_between(start_date='-2y', end_date='today')
    })

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv("data/bronze/transactions.csv", index=False)

# ---- Web/App Logs ----
num_logs = 500000
logs = []

for i in range(num_logs):
    cust_id = random.randint(1, num_customers)
    logs.append({
        "session_id": i+1,
        "customer_id": cust_id,
        "page_visited": random.choice(['Home','Product','Cart','Checkout','Support']),
        "timestamp": fake.date_time_between(start_date='-1y', end_date='now')
    })

logs_df = pd.DataFrame(logs)
logs_df.to_csv("data/bronze/web_logs.csv", index=False)

# ---- Support Tickets ----
num_tickets = 20000
tickets = []

for i in range(num_tickets):
    cust_id = random.randint(1, num_customers)
    tickets.append({
        "ticket_id": i+1,
        "customer_id": cust_id,
        "issue": random.choice(['Payment','Delivery','Product','Account']),
        "priority": random.choice(['Low','Medium','High']),
        "date": fake.date_between(start_date='-1y', end_date='today')
    })

tickets_df = pd.DataFrame(tickets)
tickets_df.to_csv("data/bronze/support_tickets.csv", index=False)

# ---- Marketing Campaign ----
num_campaigns = 50000
campaigns = []

for i in range(num_campaigns):
    cust_id = random.randint(1, num_customers)
    campaigns.append({
        "campaign_id": i+1,
        "customer_id": cust_id,
        "email_opened": random.choice([0,1]),
        "clicked_link": random.choice([0,1]),
        "campaign_date": fake.date_between(start_date='-1y', end_date='today')
    })

campaigns_df = pd.DataFrame(campaigns)
campaigns_df.to_csv("data/bronze/marketing.csv", index=False)

print("Synthetic datasets generated in data/bronze/")
