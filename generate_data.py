import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

# Database Connection String
# Syntax: postgresql://username:password@localhost:port/database_name
engine = create_engine('postgresql://postgres:your_password_here@localhost:5432/fintech_fraud_db')

print("Generating synthetic enterprise dimensions...")

# 1. Generate Dimension: Users
users = []
for i in range(100):
    users.append({
        "user_id": f"USR-{1000+i}",
        "kyc_status": random.choice(["Tier 1", "Tier 2", "Tier 3"]),
        "risk_score_baseline": round(random.uniform(10.0, 85.0), 2)
    })
df_users = pd.DataFrame(users)
df_users.to_sql('dim_users', engine, if_exists='append', index=False)

# 2. Generate Dimension: Merchants
merchants = []
categories = ["E-Commerce", "Gaming/Betting", "Crypto Exchange", "Streaming", "Food/Groceries"]
for i in range(30):
    merchants.append({
        "merchant_id": f"MERCH-{5000+i}",
        "category": random.choice(categories),
        "risk_tier": random.choice(["Low", "Medium", "High"])
    })
df_merchants = pd.DataFrame(merchants)
df_merchants.to_sql('dim_merchants', engine, if_exists='append', index=False)

print("Generating 10,000 transaction records with embedded fraud vectors...")

# 3. Generate Fact: Transactions
transactions = []
start_date = datetime.now() - timedelta(days=30)

for i in range(10000):
    user_idx = random.randint(1, 100)
    merchant_idx = random.randint(1, 30)
    tx_time = start_date + timedelta(minutes=random.randint(1, 43200))
    amount = round(np.random.exponential(scale=50.0) + 2.0, 2)
    
    # Injecting baseline fraud rules for your analysis to discover later
    is_vpn = random.choices([True, False], weights=[8, 92])[0]
    is_fraud = False
    status = "Approved"
    
    # Fraud Pattern A: High amount + VPN
    if amount > 250.0 and is_vpn:
        is_fraud = random.choices([True, False], weights=[70, 30])[0]
    
    # Fraud Pattern B: Risky Merchants (Crypto/Betting) have higher fraud rates
    if merchant_idx in [5, 12, 19]: 
        is_fraud = random.choices([True, False], weights=[15, 85])[0]
        
    if is_fraud:
        status = random.choice(["Approved", "Blocked"]) # Some caught, some missed!
        
    transactions.append({
        "user_key": user_idx,
        "merchant_key": merchant_idx,
        "timestamp": tx_time,
        "amount": amount,
        "status": status,
        "is_vpn": is_vpn,
        "is_fraud": is_fraud
    })

df_transactions = pd.DataFrame(transactions)
df_transactions.to_sql('fact_transactions', engine, if_exists='append', index=False)

print("Successfully populated PostgreSQL database with 10,000 transaction records!")
