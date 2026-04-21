import streamlit as st
import sqlite3
from utils.session_manager import get_user_email

def risk_analyst_dashboard():
    st.title("🎯 Risk Analyst Dashboard")
    user_email = get_user_email()
    
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    # Filter for 'Loan' type cases assigned to this Risk Analyst
    cursor.execute("""
        SELECT id, transaction_id, annual_income, status 
        FROM cases 
        WHERE assigned_to = ? AND case_type = 'Loan'
        ORDER BY id DESC
    """, (user_email,))
    
    cases = cursor.fetchall()

    if cases:
        for case in cases:
            case_id, app_id, income, status = case
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**Application ID:** {app_id}")
                    st.write(f"**Applicant Annual Income:** ${income:,.2f}")
                    st.write(f"**Status:** {status}")
                with col2:
                    if st.button("Review Risk", key=f"risk_btn_{case_id}"):
                        st.session_state["selected_case"] = case_id
                        st.session_state["page"] = "risk_case_detail"
                        st.rerun()
                st.divider()
    else:
        st.info("No loan applications assigned to your queue.")
    conn.close()