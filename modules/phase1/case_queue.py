import streamlit as st
import pandas as pd
from utils.data_loader import load_fraud_data, load_risk_data

def show_case_queue():
    st.title("Institutional Admin View")
    
    # Dynamic Metrics Header
    # These values shift based on which feed is selected below
    m1, m2, m3, m4 = st.columns(4)
    
    # Tabs for the different data streams
    tab1, tab2 = st.tabs(["Financial Fraud Feed", "Credit Risk Feed"])

    with tab1:
        # Update metrics for Fraud
        m1.metric("HIGH PRIORITY", "245", "Immediate Action")
        m2.metric("PENDING QUEUE", "958", "Avg. Wait: 4.2m")
        m3.metric("COMPLETED TODAY", "42", "Target: 50")
        m4.metric("SYSTEM HEALTH", "Secure", "SSL Verified")

        st.write("### Triage Queue")
        df_f = load_fraud_data(nrows=5) # Strict 5-row limit
        st.dataframe(df_f, use_container_width=True, hide_index=True)

    with tab2:
        # Update metrics for Risk
        m1.metric("RISK ALERTS", "112", "Critical Flags")
        m2.metric("APPLICATIONS", "430", "Avg. Wait: 12.5m")
        m3.metric("VERIFIED", "18", "Target: 25")
        m4.metric("RISK ENGINE", "Active", "Model v2.4")

        st.write("### Triage Queue")
        df_r = load_risk_data(nrows=5) # Strict 5-row limit
        st.dataframe(df_r, use_container_width=True, hide_index=True)

    st.divider()

    # Analyst Investigation & Review Log (Admin Monitoring Only)
    st.write("### Analyst Investigation & Review Log")
    
    log_data = {
        "Case Number": ["20000001", "20000002", "20000003", "20000004", "20000005"],
        "Model Prediction": ["98% Fraud", "Low Risk", "85% Fraud", "92% Fraud", "High Risk"],
        "Analyst Decision": ["Confirmed", "Cleared", "Dismissed", "Confirmed", "Investigating"],
        "Log Status": ["Verified", "Verified", "Verified", "Verified", "Pending"]
    }
    st.table(pd.DataFrame(log_data))