import streamlit as st

def show_employee_form():
    st.title("Employee Management")
    st.markdown("#### ONBOARD NEW INSTITUTIONAL PERSONNEL")

    # Wrapper container for the form
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter first name")
            last_name = st.text_input("Last Name", placeholder="Enter last name")
            emp_id = st.text_input("Employee ID", placeholder="e.g. FP-2026-101")
            
        with col2:
            email = st.text_input("Institutional Email", placeholder="employee@bank.com")
            # UPDATED ROLES HERE
            role = st.selectbox("System Access Role", 
                              ["Fraud and Risk Analyst", "Senior Analyst", "System Admin"])
            department = st.selectbox("Assign Department", 
                                    ["Fraud Detection Unit", "Risk Assessment", "IT Compliance"])

        st.divider()
        
        # Registration logic
        if st.button("REGISTER EMPLOYEE", type="primary", use_container_width=True):
            if first_name and last_name and email:
                st.success(f"SUCCESS: {first_name} {last_name} registered as {role}.")
                st.balloons()
            else:
                st.error("REQUIRED FIELDS MISSING: Please provide Name and Email.")

    st.divider()
    
    # Simple Audit Log Table (Mock Data)
    st.write("##### Recently Registered Personnel")
    registry_data = {
        "EMP ID": ["FP-2026-001", "FP-2026-002"],
        "Full Name": ["Rajesh Kumar", "Amit Sharma"],
        "Role": ["Fraud Analyst", "Risk Analyst", "System Admin"],
        "Status": ["Active", "Active"]
    }
    st.table(registry_data)