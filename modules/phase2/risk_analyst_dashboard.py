import streamlit as st
from utils.db_controller import execute_custom_query, save_analyst_verdict

def show_risk_analyst_dash():
    risk_id = st.session_state.get('selected_risk_id')
    if not risk_id:
        return

    st.title("Credit Risk Assessment")
    st.markdown(f"#### ANALYST WORKSPACE: CUST-{risk_id}")

    # Fetch fresh data for the specific customer
    cust = execute_custom_query(f"SELECT * FROM risk_data WHERE id = {risk_id}").iloc[0]

    # Layout into 3 distinct sections
    col_profile, col_step1, col_step2 = st.columns([1, 1.2, 1.2])

    # --- SECTION 1: PROFILE ---
    with col_profile:
        st.write("##### FINANCIAL PROFILE")
        with st.container(border=True):
            st.metric("Annual Income", f"${cust['Annual_Income']:,}")
            st.write(f"**Age:** {int(cust['Age'])}")
            st.write(f"**Credit Score:** {cust['Credit_Score']}")
            st.write(f"**Accounts:** {int(cust['Num_Bank_Accounts'])}")

    # --- SECTION 2: STEP 1 (CLASSIFICATION) ---
    with col_step1:
        st.write("##### STEP 1: ELIGIBILITY")
        with st.container(border=True):
            if st.button("RUN CLASSIFICATION", use_container_width=True, type="primary"):
                # Your Model Logic
                st.session_state['temp_elig'] = "APPROVED" if cust['Annual_Income'] > 18000 else "REJECTED"
            
            if 'temp_elig' in st.session_state:
                status = st.session_state['temp_elig']
                color = "#00CC96" if status == "APPROVED" else "#FF4B4B"
                st.markdown(f"""<div style="background-color:{color}; padding:10px; border-radius:5px; text-align:center; color:white; font-weight:bold;">
                            MODEL RESULT: {status}</div>""", unsafe_allow_html=True)
                
                # Only show manual verdict if the model finds them eligible
                if status == "APPROVED":
                    st.write("")
                    st.radio("Final Approval Verdict", ["Approve", "Reject"], key="verdict_choice")

    # --- SECTION 3: STEP 2 (REGRESSION) ---
    with col_step2:
        st.write("##### STEP 2: LOAN ALLOCATION")
        # Logic: Only unlock if Step 1 Model AND Analyst both approve
        if st.session_state.get('temp_elig') == "APPROVED":
            with st.container(border=True):
                # Regression Model Suggestion (40% of Income)
                suggested = float(cust['Annual_Income'] * 0.4)
                st.write(f"**AI Recommended Limit:** ${suggested:,.2f}")
                
                # SURPRISE SLIDER
                final_limit = st.slider("Final Amount ($)", 5000.0, suggested, suggested * 0.8)
                
                # RISK ANALYST COMMENT (Requirement Check!)
                comment = st.text_area("Analyst Justification", placeholder="Why are you granting this limit?")
                
                if st.button("FINALIZE & CLOSE CASE", use_container_width=True, type="primary"):
                    if not comment:
                        st.warning("Please provide a justification comment.")
                    else:
                        # Save to cases_resolved (This triggers the Counter Change!)
                        save_analyst_verdict(
                            case_id=risk_id,
                            case_type="Credit Risk",
                            model_verdict=f"AI Suggested ${suggested:,.0f}",
                            analyst_verdict=f"Limit: ${final_limit:,.0f}",
                            comment=comment
                        )
                        # RESET STATE & REDIRECT
                        del st.session_state['selected_risk_id']
                        if 'temp_elig' in st.session_state: del st.session_state['temp_elig']
                        st.session_state['nav'] = "Risk_Queue"
                        st.rerun()
        else:
            st.info("🔒 Step 2 (Loan Amount) is locked until Eligibility is confirmed.")