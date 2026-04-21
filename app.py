import streamlit as st
import sys
import os

# PATH RESOLUTION
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from utils.db_controller import initialize_database
from utils.session_manager import logout

st.set_page_config(page_title="FraudPulse Admin", layout="wide")
initialize_database()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'nav' not in st.session_state:
    st.session_state['nav'] = "Queue"

def main():
    if not st.session_state['logged_in']:
        from modules.auth.login import login_page
        login_page()
    else:
        with st.sidebar:
            st.title("FraudPulse")
            st.write("**ADMIN:** admin@bank.com")
            st.divider()
            
            if st.button("Case Queue", use_container_width=True):
                st.session_state['nav'] = "Queue"
            if st.button("Analytics Dashboard", use_container_width=True):
                st.session_state['nav'] = "Analytics"
            if st.button("Employee Management", use_container_width=True):
                st.session_state['nav'] = "Employees"
            
            st.divider()
            if st.button("Logout System", use_container_width=True, type="secondary"):
                st.session_state['logged_in'] = False
                logout()
                st.rerun()

        nav_choice = st.session_state.get('nav', "Queue")
        
        if nav_choice == "Queue":
            from modules.phase1.case_queue import show_case_queue
            show_case_queue()
        elif nav_choice == "Analytics":
            from modules.admin.analytics import show_analytics
            show_analytics()
        elif nav_choice == "Employees":
            from modules.admin.employee_form import show_employee_form
            show_employee_form()

if __name__ == "__main__":
    main()