import streamlit as st

print("--- Session Manager Loaded Successfully ---")

def login_user(user_data):
    """Stores user info in the session state."""
    st.session_state["logged_in"] = True
    st.session_state["user_info"] = user_data

def is_logged_in():
    """Checks if a user is currently logged in."""
    return st.session_state.get("logged_in", False)

def get_role():
    """Returns the role (admin/analyst)."""
    return st.session_state.get("user_info", {}).get("role")

def get_position():
    """Returns the specific position."""
    return st.session_state.get("user_info", {}).get("position")

def get_user_email():
    """Returns the email of the logged-in user."""
    return st.session_state.get("user_info", {}).get("email")

def logout():
    """Clears the session state."""
    st.session_state["logged_in"] = False
    st.session_state["user_info"] = {}