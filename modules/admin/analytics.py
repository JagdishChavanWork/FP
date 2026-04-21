import streamlit as st
import pandas as pd
import numpy as np

def show_analytics():
    # 1. Heading
    st.title("System Fraud Performance & Analytics Dashboard")
    st.markdown("#### PHASE 1: LIVE MODEL METRICS")

    # 2. Executive Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL FRAUD", "$1.2M")
    m2.metric("PRECISION", "94.2%")
    m3.metric("FALSE POSITIVE", "1.8%", "-0.4%", delta_color="inverse")
    m4.metric("EFFICIENCY", "1:8")

    st.divider()

    # 3. Charts Row
    c1, c2 = st.columns(2)
    with c1:
        st.write("##### Fraud Volume Trends")
        # Generating synthetic trend data
        data = pd.DataFrame(np.random.rand(30, 2), columns=['Volume', 'Fraud'])
        st.area_chart(data)
        
    with c2:
        st.write("##### Fraud by Category")
        # Visualizing the distribution of fraud types
        types = pd.DataFrame({
            "Type": ["CASH_OUT", "PAYMENT", "TRANSFER"], 
            "Cases": [450, 250, 200]
        })
        st.bar_chart(data=types, x="Type", y="Cases")

    st.divider()

    # 4. System Health Log (Strict 5-Row Table)
    st.write("##### System Health Log")
    log = pd.DataFrame({
        "Date": ["2026-04-21"] * 5,
        "Alert": ["High Velocity", "IP Mismatch", "Pattern", "Large Transfer", "Spike"],
        "Status": ["Confirmed", "Cleared", "Dismissed", "Confirmed", "Cleared"]
    })
    # Table renders a cleaner, fixed grid for your presentation
    st.table(log)

    st.caption("Admin Mode: Observation Only.")