import streamlit as st
import sqlite3
import pandas as pd
from utils.model_loader import load_model
from utils.session_manager import get_role
from services.case_service import mark_case_completed

def risk_case_detail():
    case_id = st.session_state.get("selected_case")
    if not case_id:
        st.warning("No case selected")
        return

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = cursor.fetchone()
    conn.close()

    st.title(f"Loan Risk Analysis - ID {case_id}")
    
    # Display Risk Data
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Annual Income", f"${case[13]:,.2f}")
        st.write(f"**DTI Ratio:** {case[14]}")
        st.write(f"**Monthly EMI:** ${case[15]:,.2f}")
    with col2:
        st.write(f"**Age:** {case[19]}")
        st.write(f"**Payment Stress:** {case[16]}")
        st.write(f"**Total Loans:** {case[17]}")

    st.divider()

    if st.button("Generate ML Risk Prediction"):
        # Load the saved Phase-II Models
        # Ensure your feature names match the columns in the training notebook
        approval_model = load_model("models/loan/approval_model.pkl")
        limit_model = load_model("models/loan/credit_limit_model.pkl")
        
        # Prepare input (Ensure all training features are included here)
        input_df = pd.DataFrame([{
            "Annual_Income": case[13],
            "DTI_Ratio": case[14],
            "Total_EMI_per_month": case[15],
            "Payment_Stress": case[16],
            "Num_of_Loan": case[17],
            "Monthly_Balance": case[18],
            "Age": case[19]
            # ... add any other features from your pkl list ...
        }])

        prediction = approval_model.predict(input_df)[0]
        
        if prediction == 1:
            limit = limit_model.predict(input_df)[0]
            st.success(f"ML Recommendation: APPROVED with ${limit:,.2f} limit")
            st.session_state["system_result"] = f"Approved (${limit:,.2f})"
        else:
            st.error("ML Recommendation: REJECTED")
            st.session_state["system_result"] = "Rejected"

    if "system_result" in st.session_state:
        st.divider()
        st.subheader("Analyst Final Decision")
        final_dec = st.selectbox("Your Decision", ["Approve", "Reject"])
        comments = st.text_area("Personal Comments & Justification")

        if st.button("Submit Decision"):
            mark_case_completed(case_id, st.session_state["system_result"], final_dec, comments)
            st.success("Risk Assessment Logged Successfully")
            del st.session_state["system_result"]
            
            # Navigation back
            role = get_role()
            if role == "admin": st.session_state["admin_page"] = "dashboard"
            else: st.session_state["page"] = "dashboard"
            st.rerun()

    if st.button("Return to Dashboard"):
        st.session_state["page"] = "dashboard"
        st.rerun()