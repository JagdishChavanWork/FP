import pandas as pd
import sqlite3
from datetime import datetime
import random


def generate_cases(limit=100):

    # 🔷 Load dataset (use sample for speed)
    df = pd.read_csv("data/raw/fraud_sample.csv")

    # 🔷 Filter only relevant fraud types
    df = df[df["type"].isin(["CASH_OUT", "TRANSFER"])]

    # 🔷 Take subset
    df = df.sample(n=limit, random_state=42)

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    for i, row in df.iterrows():

        # 🔷 Feature engineering (same as model)
        balanceDiffOrig = row["oldbalanceOrg"] - row["newbalanceOrig"]
        balanceDiffDest = row["newbalanceDest"] - row["oldbalanceDest"]
        type_TRANSFER = 1 if row["type"] == "TRANSFER" else 0

        # 🔷 Assign to dummy analyst (we’ll improve later)
        assigned_to = "analyst@fraudpulse.com"

        cursor.execute("""
        INSERT INTO cases (
            transaction_id,
            step,
            type,
            amount,
            oldbalanceOrg,
            newbalanceOrig,
            oldbalanceDest,
            newbalanceDest,
            isFlaggedFraud,
            balanceDiffOrig,
            balanceDiffDest,
            type_TRANSFER,
            assigned_to,
            assigned_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"TXN_{i}",
            int(row["step"]),
            row["type"],
            float(row["amount"]),
            float(row["oldbalanceOrg"]),
            float(row["newbalanceOrig"]),
            float(row["oldbalanceDest"]),
            float(row["newbalanceDest"]),
            int(row["isFlaggedFraud"]),
            float(balanceDiffOrig),
            float(balanceDiffDest),
            int(type_TRANSFER),
            assigned_to,
            datetime.now().strftime("%Y-%m-%d"),
            "Pending"
        ))

    conn.commit()
    conn.close()

    print(f"✅ {limit} cases generated successfully")