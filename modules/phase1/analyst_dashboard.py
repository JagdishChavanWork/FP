import streamlit as st
import pandas as pd
import numpy as np

def show_analytics():
    # Keep the heading and subheading exactly as confirmed
    st.title("System Fraud Performance & Analytics Dashboard")
    st.markdown("#### PHASE 1 (Synthetic Transaction Monitoring): LIVE MODEL METRICS")

    # 1. Executive Metrics (Simple, High-Contrast Native Style)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL FRAUD DETECTED", "$1.2M", delta=None)
    m2.metric("MODEL PRECISION", "94.2%", delta=None)
    m3.metric("FALSE POSITIVE RATE", "1.8%", delta="-0.4%", delta_color="inverse")
    m4.metric("SYSTEM EFFICIENCY", "1:8", delta=None)

    st.divider()

    # 2. Integrated Chart Grid (Simple Streamlit Natives)
    col1, col2 = st.columns(2)

    with col1:
        st.write("##### Fraud Volume vs. Total Transactions (Last 30 Days)")
        # Generating clean trend data
        chart_data = pd.DataFrame(
            np.random.rand(30, 2),
            columns=['Total Transactions', 'Detected Fraud']
        )
        st.area_chart(chart_data)

    with col2:
        st.write("##### Fraud Distribution by Transaction Type")
        # Bar chart is more stable than a Donut chart in basic Streamlit
        fraud_types = pd.DataFrame({
            "Type": ["CASH_OUT", "PAYMENT", "TRANSFER", "CASH_IN"],
            "Cases": [450, 250, 200, 100]
        })
        st.bar_chart(data=fraud_types, x="Type", y="Cases")

    st.divider()

    # 3. System Health & Model Alert Log (Strict 5-Row Table)
    st.write("##### System Health & Model Alert Log")
    log_df = pd.DataFrame({
        "Date": ["2026-04-21", "2026-04-20", "2026-04-20", "2026-04-19", "2026-04-19"],
        "Alert Type": ["High Velocity", "IP Mismatch", "Pattern Shift", "Large Transfer", "CASH_OUT Spike"],
        "Status": ["Confirmed", "Cleared", "Dismissed", "Confirmed", "Cleared"],
        "Resolution": ["Flagged", "Verified", "False Positive", "Blocked", "Verified"]
    })
    # Table is safer for the "Log" look than a Dataframe
    st.table(log_df)

    st.caption("Admin Mode: Observation Only. Directives can be issued via the Management Dashboard.")