import streamlit as st
import sqlite3
from utils.security import hash_password


def create_user():

    st.subheader("Create Analyst")

    name = st.text_input("Name")
    email = st.text_input("Email")
    emp_id = st.text_input("Employee ID")
    password = st.text_input("Password", type="password")

    position = st.selectbox(
        "Position",
        ["Fraud Analyst", "Risk Analyst"]
    )

    if st.button("Create User"):

        # 🔷 1. Normalize email
        email = email.lower().strip()

        # 🔷 2. Basic validation
        if not name or not email or not emp_id or not password:
            st.warning("All fields are required")
            return

        # 🔷 3. Password policy
        if len(password) < 6:
            st.warning("Password must be at least 6 characters")
            return

        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()

        # 🔷 4. Prevent duplicate users
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            st.error("User already exists with this email")
            conn.close()
            return

        # 🔷 5. Hash password
        hashed = hash_password(password)

        # 🔷 6. Insert user
        cursor.execute("""
        INSERT INTO users (name, email, employee_id, password, role, position)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, emp_id, hashed, "analyst", position))

        conn.commit()
        conn.close()

        st.success(f"{position} created successfully")