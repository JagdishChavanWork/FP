import streamlit as st
import sqlite3
from utils.session_manager import get_user_email


def analyst_dashboard():

    st.title("Fraud Analyst Dashboard")

    user_email = get_user_email()

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    # =========================================================
    # 🔷 1. Cases Assigned Today (Pending only)
    # =========================================================
    cursor.execute("""
        SELECT COUNT(*) FROM cases
        WHERE assigned_to = ? AND status = 'Pending'
    """, (user_email,))

    count = cursor.fetchone()[0]

    st.metric("Cases Assigned Today", count)

    st.divider()

    # =========================================================
    # 🔷 2. Fetch Case List
    # =========================================================
    cursor.execute("""
        SELECT id, transaction_id, amount, type, status
        FROM cases
        WHERE assigned_to = ?
        ORDER BY id DESC
    """, (user_email,))

    cases = cursor.fetchall()

    # =========================================================
    # 🔷 3. Display Cases
    # =========================================================
    if cases:

        for case in cases:

            case_id, txn_id, amount, txn_type, status = case

            with st.container():

                col1, col2 = st.columns([4, 1])

                # 🔷 Case Info
                with col1:
                    st.write(f"**Case ID:** {case_id}")
                    st.write(f"Transaction: {txn_id}")
                    st.write(f"Amount: ₹{amount:,.2f}")
                    st.write(f"Type: {txn_type}")
                    st.write(f"Status: {status}")

                # 🔷 Predict Button
                with col2:
                    if st.button("Predict", key=f"predict_{case_id}"):
                        st.session_state["selected_case"] = case_id
                        st.session_state["page"] = "case_detail"
                        st.rerun()

                st.divider()

    else:
        st.info("No cases assigned yet")

    conn.close()