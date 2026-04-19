import streamlit as st


def login(role, position):
    st.session_state["logged_in"] = True
    st.session_state["role"] = role
    st.session_state["position"] = position


def is_logged_in():
    return st.session_state.get("logged_in", False)


def get_role():
    return st.session_state.get("role")


def get_position():
    return st.session_state.get("position")


def get_user_email():
    return st.session_state.get("email")


def logout():
    st.session_state.clear()