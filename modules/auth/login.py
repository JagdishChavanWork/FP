import streamlit as st

def login_page():
    st.markdown("<h1 style='text-align: center;'>FraudPulse</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>FRAUD AND RISK ANALYSIS BANKING SYSTEM</p>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 2, 1])
    
    with col:
        with st.container(border=True):
            st.subheader("Institutional Login")
            email = st.text_input("Email", placeholder="admin@bank.com")
            password = st.text_input("Access Key", type="password")
            
            if st.button("AUTHENTICATE", use_container_width=True, type="primary"):
                if email == "admin@bank.com" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")