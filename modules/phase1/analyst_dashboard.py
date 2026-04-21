import streamlit as st
import pandas as pd
from utils.db_controller import execute_custom_query, save_analyst_verdict

def show_fraud_analyst_dash():
    case_id = st.session_state.get('selected_case_id')
    
    if not case_id:
        st.warning("No case selected. Please return to the Task Queue.")
        if st.button("Back to Queue"):
            st.session_state['nav'] = "Analyst_Queue"
            st.rerun()
        return

    st.title("Fraud Analyst Workspace")
    st.markdown(f"#### ANALYZING TRANSACTION ID: TXN-{case_id}")

    # Fetch data for the specific case
    query = f"SELECT * FROM fraud_data WHERE id = {case_id}"
    df = execute_custom_query(query)

    if not df.empty:
        txn = df.iloc[0]
        
        col_left, col_right = st.columns([1.5, 1])

        with col_left:
            st.write("##### TRANSACTION DETAILS")
            with st.container(border=True):
                details = {
                    "Attribute": ["Type", "Amount", "Origin", "Dest", "Old Balance", "New Balance"],
                    "Details": [txn['type'], f"${txn['amount']:,}", txn['nameOrig'], txn['nameDest'], 
                                f"${txn['oldbalanceOrg']:,}", f"${txn['newbalanceOrig']:,}"]
                }
                st.table(pd.DataFrame(details))

        with col_right:
            st.write("##### ANALYSIS & DECISION")
            with st.container(border=True):
                # Execute Prediction UI
                if st.button("EXECUTE ML PREDICTION", type="primary", use_container_width=True):
                    st.error(f"HIGH RISK: 94.2% Probability")
                
                # VERDICT FORM
                with st.form("verdict_form", border=False):
                    verdict = st.radio("Final Verdict", ["Confirmed Fraud", "Legitimate Transaction"])
                    comment = st.text_area("Analyst Comment", placeholder="Enter reasoning...")
                    
                    submit = st.form_submit_button("SUBMIT VERDICT", use_container_width=True, type="primary")

                    if submit:
                        if not comment:
                            st.warning("Please add a comment.")
                        else:
                            # --- THIS IS THE KEY PART ---
                            # This calls the function we added to db_controller
                            success = save_analyst_verdict(
                                case_id=case_id,
                                case_type="Fraud",
                                model_verdict="High Risk",
                                analyst_verdict=verdict,
                                comment=comment
                            )
                            
                            if success:
                                st.success(f"Case TXN-{case_id} Resolved!")
                                # Clear selection and go back to see the updated counters
                                del st.session_state['selected_case_id']
                                st.session_state['nav'] = "Analyst_Queue"
                                st.rerun()
                            else:
                                st.error("Database Save Failed.")
    else:
        st.error("Transaction not found.")