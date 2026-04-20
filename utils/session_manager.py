import streamlit as st


# =========================================================
# SET SESSION
# =========================================================
def set_session(email, role, position):

    st.session_state["logged_in"] = True
    st.session_state["email"] = email
    st.session_state["role"] = role
    st.session_state["position"] = position

    if role == "admin":
        st.session_state["admin_page"] = "dashboard"
    else:
        st.session_state["page"] = "dashboard"


# =========================================================
# GETTERS
# =========================================================
def get_user_email():
    return st.session_state.get("email")


def get_role():
    return st.session_state.get("role")


def get_position():
    return st.session_state.get("position")


def is_logged_in():
    return st.session_state.get("logged_in", False)


# =========================================================
# LOGOUT
# =========================================================
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]