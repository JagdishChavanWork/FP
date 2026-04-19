import streamlit as st
from modules.auth.auth_service import login_user
from utils.session_manager import login


def login_page():

    
    st.markdown(
        "<h1 style='text-align: center;'>FraudPulse System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; font-size:18px; font-weight:600;'>"
        "Advanced Fraud Detection and Risk Analysis for Banking"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            
            email = email.lower().strip()

            
            if not email or not password:
                st.warning("Please enter email and password")
                return

            # Authenticate
            role, position = login_user(email, password)

            if role:
                # 🔷 Store session
                login(role, position)

                # IMPORTANT: store email for dashboard filtering
                st.session_state["email"] = email

                st.success(f"Welcome {position}")
                st.rerun()

            else:
                st.error("Invalid credentials")