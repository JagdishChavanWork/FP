import sqlite3
import bcrypt

DB_PATH = "database/db.sqlite3"


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # =========================================================
    # USERS TABLE
    # =========================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password BLOB,
            role TEXT,
            position TEXT
        )
    """)

    # =========================================================
    # FRAUD CASES TABLE
    # =========================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            transaction_id TEXT,
            step INTEGER,
            type TEXT,
            amount REAL,

            oldbalanceOrg REAL,
            newbalanceOrig REAL,
            oldbalanceDest REAL,
            newbalanceDest REAL,

            isFlaggedFraud INTEGER,
            balanceDiffOrig REAL,
            balanceDiffDest REAL,
            type_TRANSFER INTEGER,

            assigned_to TEXT,

            system_prediction TEXT,
            analyst_decision TEXT,
            analyst_comments TEXT,

            status TEXT DEFAULT 'Pending',

            created_at TEXT,
            completed_at TEXT,
            duration_seconds REAL
        )
    """)

    # =========================================================
    # RISK CASES TABLE (NEW)
    # =========================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_id TEXT,

            age INTEGER,
            annual_income REAL,
            monthly_income REAL,

            num_bank_accounts INTEGER,
            num_credit_cards INTEGER,
            num_loans INTEGER,

            interest_rate REAL,
            delay_days INTEGER,
            credit_utilization REAL,

            outstanding_debt REAL,
            emi_per_month REAL,

            credit_history_age INTEGER,

            system_risk TEXT,
            analyst_decision TEXT,
            analyst_comments TEXT,

            recommended_limit REAL,
            approved_limit REAL,

            status TEXT DEFAULT 'Pending',

            created_at TEXT,
            completed_at TEXT,
            duration_seconds REAL
        )
    """)

    conn.commit()
    conn.close()


def create_default_admin():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE role = 'admin'")
    admin = cursor.fetchone()

    if not admin:
        password_hash = hash_password("admin123")

        cursor.execute("""
            INSERT INTO users (name, email, password, role, position)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Admin",
            "admin@fraudpulse.com",
            password_hash,
            "admin",
            "Admin"
        ))

        conn.commit()
        print("Default admin created")

    conn.close()


def init_db():
    create_tables()
    create_default_admin()