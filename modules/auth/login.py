import streamlit as st

def login_page():
    # 1. Header Section - Strict & Formal
    st.markdown("<h1 style='text-align: center;'>FRAUDPULSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>SECURE ANALYTIC GATEWAY</p>", unsafe_allow_html=True)
    st.write("") # Spacer

    # 2. Centralized Login Container
    # We use a narrower column layout to keep the box centered
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        with st.container(border=True):
            st.markdown("<h4 style='text-align: center; margin-bottom: 20px;'>AUTHENTICATION</h4>", unsafe_allow_html=True)
            
            # Input Fields
            email = st.text_input("Institutional Email", placeholder="email@bank.com")
            password = st.text_input("Access Key", type="password", placeholder="••••••••")
            
            st.write("") # Spacer
            
            # 3. Authentication Logic
            if st.button("AUTHENTICATE", use_container_width=True, type="primary"):
                
                # --- ROLE: SYSTEM ADMIN ---
                if email == "admin@bank.com" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "Admin"
                    st.session_state['email'] = email
                    st.session_state['nav'] = "Queue" # Admin landing page
                    st.success("Admin Session Verified.")
                    st.rerun()
                
                # --- ROLE: FRAUD ANALYST ---
                elif email == "fraud@bank.com" and password == "fraud123":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "Fraud Analyst"
                    st.session_state['email'] = email
                    # Redirecting to the Task Queue (the new entry point)
                    st.session_state['nav'] = "Analyst_Queue" 
                    st.success("Analyst Session Verified.")
                    st.rerun()

                # --- ROLE: RISK ANALYST ---
                elif email == "risk@bank.com" and password == "risk123":
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = "Risk Analyst"
                    st.session_state['email'] = email
                    st.session_state['nav'] = "Risk_Queue"
                    st.success("Risk Portal Verified.")
                    st.rerun()
                
                else:
                    st.error("INVALID CREDENTIALS: Access Denied.")

    # 4. Footer
    st.write("")
    st.markdown("<p style='text-align: center; font-size: 12px; color: #999;'>Property of FraudPulse Inc. v2024.1</p>", unsafe_allow_html=True)