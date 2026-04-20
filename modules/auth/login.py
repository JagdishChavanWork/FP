import streamlit as st
from modules.auth.auth_service import login_user
from utils.session_manager import set_session


def login_page():

    st.title("FraudPulse System")
    st.subheader("Login")

    with st.form("login_form"):

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Login")

        if submit:

            email = email.strip()
            password = password.strip()

            if not email or not password:
                st.warning("Please enter email and password")
                return

            role, position = login_user(email, password)

            if role:
                set_session(email, role, position)

                if role == "admin":
                    st.session_state["admin_page"] = "dashboard"
                else:
                    st.session_state["page"] = "dashboard"

                st.rerun()

            else:
                st.error("Invalid credentials")