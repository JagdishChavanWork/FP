import streamlit as st
import sqlite3
import pandas as pd

from utils.model_loader import load_model
from utils.session_manager import get_role
from services.case_service import mark_case_completed


DB_PATH = "database/db.sqlite3"


def get_case_by_id(case_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    case = cursor.fetchone()

    conn.close()
    return case


def case_detail():

    case_id = st.session_state.get("selected_case")

    if not case_id:
        st.warning("No case selected")
        return

    # =========================================================
    # LOAD CASE
    # =========================================================
    case = get_case_by_id(case_id)

    if not case:
        st.error("Case not found")
        return

    # =========================================================
    # DISPLAY CASE INFO
    # =========================================================
    st.title(f"Case Detail - ID {case_id}")

    st.subheader("Transaction Details")

    st.write(f"Transaction ID: {case[1]}")
    st.write(f"Step: {case[2]}")
    st.write(f"Type: {case[3]}")
    st.write(f"Amount: ₹{case[4]:,.2f}")

    st.write(f"Old Balance (Sender): {case[5]}")
    st.write(f"New Balance (Sender): {case[6]}")
    st.write(f"Old Balance (Receiver): {case[7]}")
    st.write(f"New Balance (Receiver): {case[8]}")

    st.divider()

    # =========================================================
    # LOAD MODEL
    # =========================================================
    model_data = load_model("models/fraud/fraud_model.pkl")

    if isinstance(model_data, dict):
        model = model_data.get("model")
    else:
        model = model_data

    # =========================================================
    # FRAUD CHECK
    # =========================================================
    st.subheader("Fraud Analysis")

    if st.button("Check Fraud"):

        input_df = pd.DataFrame([{
            "step": case[2],
            "amount": case[4],
            "oldbalanceOrg": case[5],
            "newbalanceOrig": case[6],
            "oldbalanceDest": case[7],
            "newbalanceDest": case[8],
            "isFlaggedFraud": case[9],
            "balanceDiffOrig": case[10],
            "balanceDiffDest": case[11],
            "type_TRANSFER": case[12]
        }])

        prediction = model.predict(input_df)[0]

        result = "Fraudulent" if prediction == 1 else "Non-Fraudulent"

        st.session_state["system_result"] = result

        if prediction == 1:
            st.error("High Risk Transaction")
        else:
            st.success("Low Risk Transaction")

    # =========================================================
    # ANALYST DECISION (FIXED SECTION)
    # =========================================================
    if "system_result" in st.session_state:

        st.divider()
        st.subheader("Final Decision")

        analyst_decision = st.radio(
            "Select Fraud Type",
            ["Fraudulent", "Non-Fraudulent"]
        )

        comments = st.text_area("Analyst Comments")

        if st.button("Submit Decision"):

            mark_case_completed(
                case_id,
                st.session_state["system_result"],
                analyst_decision,
                comments
            )

            st.success("Case updated successfully")

            del st.session_state["system_result"]

            go_back()

    # =========================================================
    # BACK BUTTON (ALWAYS AVAILABLE)
    # =========================================================
    st.divider()

    if st.button("Back to Dashboard"):
        go_back()


# =========================================================
# NAVIGATION HANDLER
# =========================================================
def go_back():

    role = get_role()

    if role == "admin":
        st.session_state["admin_page"] = "dashboard"
    else:
        st.session_state["page"] = "dashboard"

    st.rerun()