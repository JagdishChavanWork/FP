import streamlit as st
import sys
import os

# Ensure the root directory is in the path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.db_controller import initialize_database
from utils.session_manager import logout

# --- INITIALIZATION ---
st.set_page_config(
    page_title="FraudPulse | Institutional Gateway", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize Database on startup
initialize_database()

# Session State Defaults
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'nav' not in st.session_state:
    st.session_state['nav'] = "Home"

def main():
    # --- UNAUTHENTICATED: LOGIN PAGE ---
    if not st.session_state['logged_in']:
        from modules.auth.login import login_page
        login_page()
    
    # --- AUTHENTICATED: DASHBOARD SHELL ---
    else:
        role = st.session_state.get('role')
        email = st.session_state.get('email', 'User')

        # SIDEBAR NAVIGATION
        with st.sidebar:
            st.markdown(f"### FRAUDPULSE")
            st.info(f"**{role}**\n\n{email}")
            st.divider()
            
            # 1. Admin Navigation (Modules/Admin)
            if role == "Admin":
                if st.button("Global Case Queue", use_container_width=True): 
                    st.session_state['nav'] = "Queue"
                if st.button("System Analytics", use_container_width=True): 
                    st.session_state['nav'] = "Analytics"
                if st.button("User Management", use_container_width=True): 
                    st.session_state['nav'] = "Employees"
            
            # 2. Fraud Analyst Navigation (Modules/Phase1)
            elif role == "Fraud Analyst":
                if st.button("Task Queue", use_container_width=True):
                    if 'selected_case_id' in st.session_state:
                        del st.session_state['selected_case_id']
                    st.session_state['nav'] = "Analyst_Queue"

            # 3. Risk Analyst Navigation (Modules/Phase2)
            elif role == "Risk Analyst":
                if st.button("Task Queue", use_container_width=True):
                    # Reset specific case selection when returning to queue
                    if 'selected_risk_id' in st.session_state:
                        del st.session_state['selected_risk_id']
                    st.session_state['nav'] = "Risk_Queue"

            st.divider()
            if st.button("Logout", use_container_width=True, type="secondary"):
                st.session_state.clear()
                st.rerun()

        # --- MAIN ROUTING ENGINE ---
        nav_choice = st.session_state.get('nav')

        # ADMIN ROUTES
        if nav_choice == "Queue":
            from modules.phase1.case_queue import show_case_queue
            show_case_queue()
        elif nav_choice == "Analytics":
            from modules.admin.analytics import show_analytics
            show_analytics()
        elif nav_choice == "Employees":
            from modules.admin.employee_form import show_employee_form
            show_employee_form()
            
        # FRAUD ANALYST ROUTES (Phase 1)
        elif nav_choice == "Analyst_Queue":
            if 'selected_case_id' in st.session_state:
                from modules.phase1.analyst_dashboard import show_fraud_analyst_dash
                show_fraud_analyst_dash()
            else:
                from modules.phase1.case_queue import show_analyst_task_queue
                show_analyst_task_queue()

        # RISK ANALYST ROUTES (Phase 2)
        elif nav_choice == "Risk_Queue":
            if 'selected_risk_id' in st.session_state:
                # Correctly mapping to Phase 2 for Risk Analyst Dashboard
                from modules.phase2.risk_analyst_dashboard import show_risk_analyst_dash
                show_risk_analyst_dash()
            else:
                # The queue logic remains in Phase 1 for now
                from modules.phase1.case_queue import show_risk_task_queue
                show_risk_task_queue()
        
        # DEFAULT LANDING PAGE
        else:
            st.title(f"Welcome back, {role}")
            st.write("---")
            st.write("Select a task from the sidebar to begin your institutional review.")

if __name__ == "__main__":
    main()