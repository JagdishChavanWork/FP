import streamlit as st
import pandas as pd
import plotly.express as px

def risk_global_dashboard():
    st.title("📈 Credit Risk Intelligence")
    
    # In a real app, this loads from the big dataset
    df = pd.read_csv("loan_data.csv") # Assuming your loan dataset name

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg DTI Ratio", f"{df['DTI_Ratio'].mean():.2f}")
    col2.metric("Total Loan Volume", f"₹{df['Annual_Income'].sum()*0.2:,.0f}")
    col3.metric("High Risk Applicants", f"{len(df[df['DTI_Ratio'] > 0.4])}")

    st.divider()

    tab1, tab2 = st.tabs(["Income vs Risk", "Debt Distribution"])
    
    with tab1:
        fig = px.scatter(df.head(1000), x="Annual_Income", y="DTI_Ratio", color="Num_of_Loan",
                         title="Credit Portfolio Analysis")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig2 = px.histogram(df, x="Num_of_Loan", title="Active Loans per Applicant")
        st.plotly_chart(fig2, use_container_width=True)