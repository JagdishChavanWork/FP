import streamlit as st
import sqlite3
import numpy as np
import joblib # Using joblib to match our training script
from services.case_service import mark_case_completed

def case_detail():
    case_id = st.session_state.get("selected_case")
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = cursor.fetchone()
    conn.close()

    st.title("🔍 Transaction Audit Deep-Dive")
    
    # 1. Visual Top Bar
    cols = st.columns([1,1,1,1])
    cols[0].metric("Amount", f"₹{case[4]:,.2f}")
    cols[1].metric("Type", case[3])
    cols[2].metric("Origin Balance", f"₹{case[5]:,.2f}")
    cols[3].metric("Dest Balance", f"₹{case[8]:,.2f}")

    st.divider()

    # 2. AI Risk Scan
    st.subheader("🤖 AI Forensic Analysis")
    if st.button("🚀 Run Neural Risk Scan", use_container_width=True):
        with st.spinner("Analyzing transaction patterns..."):
            try:
                # Load the dictionary-wrapped model we just trained
                data = joblib.load("models/fraud/fraud_model.pkl")
                model = data['model']
                
                # Feature Prep
                features = np.array([[
                    case[2], case[4], case[5], case[6], 
                    case[7], case[8], case[9], case[10], 
                    case[11], case[12]
                ]])

                prediction = model.predict(features)[0]
                prob = model.predict_proba(features)[0][1] # Get fraud probability

                st.session_state["sys_res"] = "Fraudulent" if prediction == 1 else "Safe"
                st.session_state["risk_score"] = prob * 100

            except Exception as e:
                st.error(f"Scan failed: {e}")

    # 3. Visual Risk Result
    if "sys_res" in st.session_state:
        score = st.session_state["risk_score"]
        if score > 70:
            st.error(f"🚨 CRITICAL RISK DETECTED: {score:.1f}% Match with Fraud Patterns")
        elif score > 30:
            st.warning(f"⚠️ MODERATE RISK: {score:.1f}% Suspicious Activity")
        else:
            st.success(f"✅ LOW RISK: {score:.1f}% Probability of Legitimacy")

    st.divider()

    # 4. Analyst Final Verdict
    st.subheader("✍️ Analyst Determination")
    verdict = st.radio("Select Final Action:", ["Approve Transaction", "Flag as Fraud & Freeze Account"])
    comments = st.text_area("Audit Notes", placeholder="Why are you making this decision?")

    c1, c2 = st.columns(2)
    if c1.button("💾 Submit Decision", type="primary", use_container_width=True):
        sys_res = st.session_state.get("sys_res", "Not Run")
        mark_case_completed(case_id, sys_res, verdict, comments)
        st.success("Decision Logged to Core Banking System")
        st.session_state["page"] = "dashboard"
        st.rerun()
    
    if c2.button("🔙 Return to Queue", use_container_width=True):
        st.session_state["page"] = "dashboard"
        st.rerun()