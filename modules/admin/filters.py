import streamlit as st


def apply_common_filters(df, key_prefix="default"):
    """
    Apply reusable filters with unique keys to avoid widget conflicts.
    """

    st.sidebar.header("Filters")

    df_filtered = df.copy()

    # =========================================================
    # TRANSACTION TYPE FILTER
    # =========================================================
    if "type" in df_filtered.columns:
        types = sorted(df_filtered["type"].dropna().unique())

        selected_types = st.sidebar.multiselect(
            "Transaction Type",
            options=types,
            default=types,
            key=f"{key_prefix}_type"
        )

        df_filtered = df_filtered[df_filtered["type"].isin(selected_types)]

    # =========================================================
    # STATUS FILTER
    # =========================================================
    if "status" in df_filtered.columns:
        statuses = sorted(df_filtered["status"].dropna().unique())

        selected_status = st.sidebar.multiselect(
            "Case Status",
            options=statuses,
            default=statuses,
            key=f"{key_prefix}_status"
        )

        df_filtered = df_filtered[df_filtered["status"].isin(selected_status)]

    # =========================================================
    # FRAUD FILTER
    # =========================================================
    if "isFraud" in df_filtered.columns:
        fraud_filter = st.sidebar.selectbox(
            "Fraud Filter",
            ["All", "Fraud", "Non-Fraud"],
            key=f"{key_prefix}_fraud"
        )

        if fraud_filter == "Fraud":
            df_filtered = df_filtered[df_filtered["isFraud"] == 1]
        elif fraud_filter == "Non-Fraud":
            df_filtered = df_filtered[df_filtered["isFraud"] == 0]

    # =========================================================
    # AMOUNT FILTER
    # =========================================================
    if "amount" in df_filtered.columns:
        min_amt = float(df_filtered["amount"].min())
        max_amt = float(df_filtered["amount"].max())

        amount_range = st.sidebar.slider(
            "Amount Range",
            min_value=min_amt,
            max_value=max_amt,
            value=(min_amt, max_amt),
            key=f"{key_prefix}_amount"
        )

        df_filtered = df_filtered[
            (df_filtered["amount"] >= amount_range[0]) &
            (df_filtered["amount"] <= amount_range[1])
        ]

    # =========================================================
    # TIME FILTER
    # =========================================================
    if "step" in df_filtered.columns:
        min_step = int(df_filtered["step"].min())
        max_step = int(df_filtered["step"].max())

        step_range = st.sidebar.slider(
            "Time (Step Range)",
            min_value=min_step,
            max_value=max_step,
            value=(min_step, max_step),
            key=f"{key_prefix}_step"
        )

        df_filtered = df_filtered[
            (df_filtered["step"] >= step_range[0]) &
            (df_filtered["step"] <= step_range[1])
        ]

    # =========================================================
    # RESET BUTTON (UNIQUE KEY)
    # =========================================================
    if st.sidebar.button("Reset Filters", key=f"{key_prefix}_reset"):
        st.rerun()

    return df_filtered