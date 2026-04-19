import streamlit as st
import pandas as pd
import sqlite3

from modules.admin.charts import *
from modules.admin.filters import apply_common_filters


def fraud_global_dashboard():

    st.title("Fraud Intelligence Dashboard")

    # Load historical data
    df_hist = pd.read_csv("data/raw/fraud_sample.csv")

    # Load live system data
    conn = sqlite3.connect("database/db.sqlite3")
    df_cases = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()

    # Prepare historical data
    df_hist_clean = df_hist[[
        "step", "type", "amount", "isFraud"
    ]].copy()

    # Prepare live data
    df_cases_clean = df_cases[[
        "step", "type", "amount"
    ]].copy()

    df_cases_clean["isFraud"] = None

    # Combine both datasets
    df_combined = pd.concat(
        [df_hist_clean, df_cases_clean],
        ignore_index=True
    )

    # Apply filters (unique key prefix)
    df_filtered = apply_common_filters(df_combined, key_prefix="fraud")

    # KPI Section
    st.header("Key Metrics")

    total_txn = len(df_filtered)

    df_hist_filtered = df_filtered[df_filtered["isFraud"].notna()]

    fraud_count = int(df_hist_filtered["isFraud"].sum()) if not df_hist_filtered.empty else 0
    fraud_rate = (fraud_count / len(df_hist_filtered) * 100) if len(df_hist_filtered) > 0 else 0

    total_amount = df_filtered["amount"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", f"{total_txn:,}")
    col2.metric("Fraud Cases", f"{fraud_count:,}")
    col3.metric("Fraud Rate (%)", f"{fraud_rate:.2f}")
    col4.metric("Total Amount", f"{total_amount:,.0f}")

    st.divider()

    # Univariate Analysis
    st.header("Univariate Analysis")

    col1, col2 = st.columns(2)

    with col1:
        donut_chart(df_filtered["type"], "Transaction Type Distribution")

    with col2:
        if not df_hist_filtered.empty:
            donut_chart(df_hist_filtered["isFraud"], "Fraud vs Non-Fraud")
        else:
            st.info("No fraud data available for selected filters")

    col3, col4 = st.columns(2)

    with col3:
        histogram(df_filtered["amount"], "Transaction Amount Distribution")

    with col4:
        line_trend(df_filtered, "step", "Transactions Over Time")

    st.divider()

    # Bivariate Analysis
    st.header("Bivariate Analysis")

    col5, col6 = st.columns(2)

    with col5:
        if not df_hist_filtered.empty:
            box_plot(df_hist_filtered, "isFraud", "amount", "Amount vs Fraud")
        else:
            st.info("No fraud data available")

    with col6:
        if not df_hist_filtered.empty:
            pivot = pd.crosstab(
                df_hist_filtered["type"],
                df_hist_filtered["isFraud"]
            )
            st.bar_chart(pivot)
        else:
            st.info("No comparison available")

    st.divider()

    # Multivariate Analysis
    st.header("Multivariate Analysis")

    numeric_df = df_filtered.select_dtypes(include=["int64", "float64"])

    if not numeric_df.empty:
        correlation_heatmap(numeric_df)
    else:
        st.info("No numeric data available")

    st.divider()

    # Live system feed
    st.header("Live Case Feed")

    if not df_cases.empty:
        st.dataframe(
            df_cases.sort_values(by="id", ascending=False).head(20),
            use_container_width=True
        )
    else:
        st.info("No live cases available")