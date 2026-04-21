import streamlit as st
import pandas as pd
import numpy as np

def show_analytics():
    st.title("System Fraud Performance & Analytics Dashboard")
    st.markdown("#### PHASE 1: LIVE MODEL METRICS")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL FRAUD", "$1.2M")
    m2.metric("PRECISION", "94.2%")
    m3.metric("FALSE POSITIVE", "1.8%", "-0.4%", delta_color="inverse")
    m4.metric("EFFICIENCY", "1:8")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.write("##### Fraud Volume Trends")
        data = pd.DataFrame(np.random.rand(30, 2), columns=['Volume', 'Fraud'])
        st.area_chart(data)
    with c2:
        st.write("##### Fraud by Category")
        types = pd.DataFrame({"Type": ["CASH_OUT", "PAYMENT", "TRANSFER"], "Cases": [450, 250, 200]})
        st.bar_chart(data=types, x="Type", y="Cases")

    st.divider()
    st.write("##### System Health Log")
    log = pd.DataFrame({
        "Date": ["2026-04-21"] * 5,
        "Alert": ["High Velocity", "IP Mismatch", "Pattern", "Large Transfer", "Spike"],
        "Status": ["Confirmed", "Cleared", "Dismissed", "Confirmed", "Cleared"]
    })
    st.table(log)