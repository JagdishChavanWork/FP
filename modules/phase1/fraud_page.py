import streamlit as st
import numpy as np
from services.model_service import load_fraud_model
from datetime import datetime
import pandas as pd
from pathlib import Path


def fraud_page():

    st.title("Fraud Detection System")
    st.divider()

    st.subheader("Enter Transaction Details")

    # 🔷 INPUTS
    step = st.number_input("Step (Time)", min_value=1, value=1)

    transaction_type = st.selectbox(
        "Transaction Type",
        ["CASH_OUT", "TRANSFER"]
    )

    amount = st.number_input("Transaction Amount", min_value=0.0)

    oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0)
    newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0)

    oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0)

    # 🔷 BUTTON
    if st.button("Check Fraud", use_container_width=True):

        # 🔷 INPUT VALIDATION
        if newbalanceOrig > oldbalanceOrg:
            st.warning("⚠️ Invalid sender balance (New > Old)")
            return

        if newbalanceDest < oldbalanceDest:
            st.warning("⚠️ Invalid receiver balance (New < Old)")
            return

        model = load_fraud_model()

        # 🔷 FEATURE ENGINEERING
        balanceDiffOrig = oldbalanceOrg - newbalanceOrig
        balanceDiffDest = newbalanceDest - oldbalanceDest

        type_TRANSFER = 1 if transaction_type == "TRANSFER" else 0

        features = np.array([[
            step,
            amount,
            oldbalanceOrg,
            newbalanceOrig,
            oldbalanceDest,
            newbalanceDest,
            0,  # isFlaggedFraud
            balanceDiffOrig,
            balanceDiffDest,
            type_TRANSFER
        ]])

        # 🔷 PREDICTION
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        st.divider()

        # 🔷 OUTPUT
        if prediction == 1:
            st.error("🚨 Fraudulent Transaction Detected")
        else:
            st.success("✅ Transaction is Safe")

        st.info(f"Fraud Probability: {probability:.2f}")

        # 🔷 LOGGING (SAVE FOR DASHBOARD)
        log_data = {
            "timestamp": datetime.now(),
            "step": step,
            "type": transaction_type,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest,
            "prediction": int(prediction),
            "probability": probability
        }

        log_df = pd.DataFrame([log_data])

        log_path = Path("logs/fraud_logs.csv")

        if log_path.exists():
            log_df.to_csv(log_path, mode='a', header=False, index=False)
        else:
            log_df.to_csv(log_path, index=False)