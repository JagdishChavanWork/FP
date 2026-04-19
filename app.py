import streamlit as st

from database.init_db import init_db
from modules.auth.login import login_page

from utils.session_manager import (
    is_logged_in,
    get_role,
    get_position,
    logout
)

from modules.admin.user_management import create_user
from modules.admin.admin_dashboard import admin_dashboard
from modules.admin.fraud_global_dashboard import fraud_global_dashboard

from modules.phase1.analyst_dashboard import analyst_dashboard
from modules.phase1.case_detail import case_detail


st.set_page_config(
    page_title="FraudPulse System",
    layout="wide"
)

init_db()


if not is_logged_in():
    login_page()

else:
    role = get_role()
    position = get_position()

    st.sidebar.title("FraudPulse System")

    menu = st.sidebar.radio(
        "Navigation",
        ["Home", "Logout"]
    )

    if menu == "Logout":
        logout()
        st.rerun()

    # =====================================================
    # ADMIN FLOW
    # =====================================================
    if role == "admin":

        page = st.session_state.get("admin_page", "dashboard")

        if page == "case_detail":
            case_detail()

        else:
            st.subheader("Admin Panel")

            tab1, tab2, tab3 = st.tabs([
                "User Management",
                "Fraud Intelligence",
                "Operations Dashboard"
            ])

            with tab1:
                create_user()

            with tab2:
                fraud_global_dashboard()

            with tab3:
                admin_dashboard()

    # =====================================================
    # ANALYST FLOW
    # =====================================================
    elif role == "analyst":

        page = st.session_state.get("page", "dashboard")

        if position == "Fraud Analyst":

            if page == "dashboard":
                analyst_dashboard()

            elif page == "case_detail":
                case_detail()

            else:
                st.error("Invalid page state")

        else:
            st.warning("Module not available")

    # =====================================================
    # FALLBACK
    # =====================================================
    else:
        st.error("Invalid role")