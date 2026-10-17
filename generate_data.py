"""
Synthetic Dataset Generator for ScamGuard-Z
Generates realistic normal, borderline, and high-coercion transaction scenarios
for training and evaluating the ScamGuard-Z prototype on IBM LinuxONE.
"""

import pandas as pd
import numpy as np
from risk_engine import evaluate_transaction

def generate_synthetic_transactions(n_samples: int = 600) -> pd.DataFrame:
    """
    Generates synthetic transaction logs across three balanced profiles:
    - 300 Normal routine payments
    - 150 Borderline / atypical payments (e.g. buying furniture/car repair)
    - 150 Coercion / Social-Engineering payments (e.g. 'digital arrest' scams)
    """
    np.random.seed(42)
    records = []
    
    # Profile 1: Normal Routine Transactions (Low Risk)
    for i in range(300):
        avg_amt = np.random.uniform(50, 200)
        amount = np.random.uniform(10, avg_amt * 1.5)
        balance = np.random.uniform(1000, 5000)
        recip_age = np.random.uniform(100, 2000) # old recipient
        prior_tx = np.random.randint(1, 20)
        vel_today = np.random.choice([0, 1], p=[0.7, 0.3])
        recip_name = np.random.choice(["Supermarket", "Electric Utility", "Corner Cafe", "Landlord", "Phone Carrier"])
        
        eval_result = evaluate_transaction(
            amount=amount,
            avg_amount=avg_amt,
            recipient_name=recip_name,
            recipient_age_hours=recip_age,
            prior_transfers=prior_tx,
            transfers_today=vel_today,
            account_balance=balance
        )
        
        records.append({
            "transaction_id": f"TX-NORM-{i+1:04d}",
            "profile": "Normal Routine",
            "amount": round(amount, 2),
            "historical_avg_amount": round(avg_amt, 2),
            "account_balance": round(balance, 2),
            "recipient_name": recip_name,
            "recipient_age_hours": round(recip_age, 1),
            "prior_transfers_to_recipient": prior_tx,
            "transfers_in_last_24h": vel_today,
            "depletion_ratio": round(amount / balance, 3),
            "risk_score": eval_result["risk_score"],
            "risk_tier": eval_result["risk_tier"]
        })
    
    # Profile 2: Borderline / Legitimate High-Value (Medium Risk)
    for i in range(150):
        avg_amt = np.random.uniform(100, 300)
        amount = np.random.uniform(avg_amt * 2.0, avg_amt * 3.5) # higher amount
        balance = np.random.uniform(3000, 10000)
        recip_age = np.random.uniform(24, 150)
        prior_tx = np.random.choice([0, 1, 2], p=[0.4, 0.4, 0.2])
        vel_today = np.random.choice([1, 2], p=[0.8, 0.2])
        recip_name = np.random.choice(["Auto Repair Center", "Furniture Store", "Dental Clinic", "Travel Agency"])
        
        eval_result = evaluate_transaction(
            amount=amount,
            avg_amount=avg_amt,
            recipient_name=recip_name,
            recipient_age_hours=recip_age,
            prior_transfers=prior_tx,
            transfers_today=vel_today,
            account_balance=balance
        )
        
        records.append({
            "transaction_id": f"TX-BORD-{i+1:04d}",
            "profile": "Borderline / Legitimate High-Value",
            "amount": round(amount, 2),
            "historical_avg_amount": round(avg_amt, 2),
            "account_balance": round(balance, 2),
            "recipient_name": recip_name,
            "recipient_age_hours": round(recip_age, 1),
            "prior_transfers_to_recipient": prior_tx,
            "transfers_in_last_24h": vel_today,
            "depletion_ratio": round(amount / balance, 3),
            "risk_score": eval_result["risk_score"],
            "risk_tier": eval_result["risk_tier"]
        })

    # Profile 3: Coercion / Digital Arrest / Elder Extortion (High Risk)
    for i in range(150):
        avg_amt = np.random.uniform(100, 400)
        balance = np.random.uniform(4000, 12000)
        amount = np.random.uniform(balance * 0.82, balance * 0.98) # drains 80-98%
        recip_age = np.random.uniform(0.5, 12.0) # added hours ago!
        prior_tx = 0 # brand new recipient!
        vel_today = np.random.choice([1, 2, 3, 4], p=[0.3, 0.3, 0.2, 0.2])
        recip_name = np.random.choice(["Central Escrow Vault", "CBI Clearance Office", "Safe Holding Acct 809", "Secure Legal Deposit"])
        
        eval_result = evaluate_transaction(
            amount=amount,
            avg_amount=avg_amt,
            recipient_name=recip_name,
            recipient_age_hours=recip_age,
            prior_transfers=prior_tx,
            transfers_today=vel_today,
            account_balance=balance
        )
        
        records.append({
            "transaction_id": f"TX-SCAM-{i+1:04d}",
            "profile": "Coercion / Digital Arrest",
            "amount": round(amount, 2),
            "historical_avg_amount": round(avg_amt, 2),
            "account_balance": round(balance, 2),
            "recipient_name": recip_name,
            "recipient_age_hours": round(recip_age, 1),
            "prior_transfers_to_recipient": prior_tx,
            "transfers_in_last_24h": vel_today,
            "depletion_ratio": round(amount / balance, 3),
            "risk_score": eval_result["risk_score"],
            "risk_tier": eval_result["risk_tier"]
        })
        
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_synthetic_transactions(600)
    df.to_csv("synthetic_transactions.csv", index=False)
    print(f"Generated {len(df)} synthetic transactions saved to synthetic_transactions.csv")
    print("\nSummary Statistics by Profile:")
    print(df.groupby("profile")[["risk_score", "depletion_ratio"]].agg(["mean", "min", "max"]))
    print("\nDistribution across Risk Tiers:")
    print(pd.crosstab(df["profile"], df["risk_tier"]))
