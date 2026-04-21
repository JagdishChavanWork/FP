import streamlit as st
import pandas as pd
from utils.db_controller import execute_custom_query

# ==========================================
# 1. ADMIN VIEW: Global System Overview
# ==========================================
def show_case_queue():
    st.title("Global Case Management")
    st.markdown("#### SYSTEM-WIDE PENDING TASKS")

    # Mapping to your specific CSV table names
    f_pending = execute_custom_query("SELECT id, 'Fraud' as dept, amount as val FROM fraud_sample WHERE id NOT IN (SELECT case_id FROM cases_resolved WHERE type='Fraud Detection') LIMIT 10")
    r_pending = execute_custom_query("SELECT id, 'Risk' as dept, Annual_Income as val FROM credit_risk_production_final WHERE id NOT IN (SELECT case_id FROM cases_resolved WHERE type='Credit Risk') LIMIT 10")
    
    combined = pd.concat([f_pending, r_pending], ignore_index=True)
    
    if not combined.empty:
        st.dataframe(combined, use_container_width=True, hide_index=True)
    else:
        st.success("All queues are clear!")

# ==========================================
# 2. FRAUD ANALYST VIEW: Phase 1
# ==========================================
def show_analyst_task_queue():
    st.title("Fraud Analyst Workspace")
    st.markdown("#### PENDING FRAUD INVESTIGATIONS")

    # Using fraud_sample table
    query = """
        SELECT id, amount, merchant, category 
        FROM fraud_sample 
        WHERE id NOT IN (SELECT case_id FROM cases_resolved WHERE type = 'Fraud Detection')
        LIMIT 15
    """
    df = execute_custom_query(query)

    if not df.empty:
        for _, row in df.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 2, 1])
                # Note: Adjust 'amount' column name if it differs in your CSV
                c1.write(f"**TXN-{row['id']}** | **Amt:** ${row['amount']}")
                c2.write(f"**Merchant:** {row['merchant']}")
                if c3.button("INVESTIGATE", key=f"f_{row['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_case_id'] = row['id']
                    st.rerun()
    else:
        st.info("No pending fraud cases in 'fraud_sample' table.")

# ==========================================
# 3. RISK ANALYST VIEW: Phase 2
# ==========================================
def show_risk_task_queue():
    st.title("Risk Analyst Workspace")
    st.markdown("#### CREDIT REVIEW QUEUE")

    # Using credit_risk_production_final table
    total_r = execute_custom_query("SELECT count(*) as count FROM credit_risk_production_final").iloc[0]['count']
    done_r = len(execute_custom_query("SELECT case_id FROM cases_resolved WHERE type = 'Credit Risk'"))
    
    m1, m2 = st.columns(2)
    m1.metric("PENDING", total_r - done_r)
    m2.metric("COMPLETED", done_r)

    query = """
        SELECT id, Annual_Income, Credit_Score 
        FROM credit_risk_production_final 
        WHERE id NOT IN (SELECT case_id FROM cases_resolved WHERE type = 'Credit Risk')
        LIMIT 15
    """
    df = execute_custom_query(query)

    if not df.empty:
        for _, row in df.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 2, 1])
                c1.write(f"**CUST-{row['id']}** | **Income:** ${row['Annual_Income']:,}")
                c2.write(f"**Score:** {row['Credit_Score']}")
                if c3.button("WORK CASE", key=f"risk_{row['id']}", use_container_width=True, type="primary"):
                    st.session_state['selected_risk_id'] = row['id']
                    st.rerun()