import streamlit as st
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAUD_PATH = os.path.join(BASE_DIR, "data", "raw", "fraud_sample.csv")
RISK_PATH = os.path.join(BASE_DIR, "data", "raw", "credit_risk_production_final.csv")

@st.cache_data(ttl=3600)
def load_fraud_data(nrows=1000):
    if os.path.exists(FRAUD_PATH):
        return pd.read_csv(FRAUD_PATH, nrows=nrows)
    # FAIL-SAFE: Generate presentation-ready mock data if file is missing
    return pd.DataFrame({
        'step': np.random.randint(1, 700, nrows),
        'type': np.random.choice(['PAYMENT', 'TRANSFER', 'CASH_OUT'], nrows),
        'amount': np.random.uniform(1000, 500000, nrows),
        'nameOrig': [f'C{i}' for i in range(nrows)],
        'isFraud': np.random.choice([0, 1], nrows, p=[0.95, 0.05])
    })

@st.cache_data(ttl=3600)
def load_risk_data(nrows=1000):
    if os.path.exists(RISK_PATH):
        return pd.read_csv(RISK_PATH, nrows=nrows)
    # FAIL-SAFE: Presentation data
    return pd.DataFrame({
        'Age': np.random.randint(18, 70, nrows),
        'Annual_Income': np.random.uniform(20000, 150000, nrows),
        'Credit_Score': np.random.choice(['Good', 'Poor', 'Standard'], nrows),
        'Risk_Score_Proxy': np.random.uniform(0, 1, nrows)
    })