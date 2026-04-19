import streamlit as st
from modules.auth.auth_service import create_user

def admin_register():

    st.subheader("Create New User")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    role = st.selectbox("Role", ["fraud", "risk"])

    if st.button("Create User"):

        success = create_user(username, password, role)

        if success:
            st.success("User created successfully")
        else:
            st.error("User already exists")