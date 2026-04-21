import sqlite3

def init_db():
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT,
            position TEXT
        )
    ''')

    # Expanded Cases Table to handle both Fraud and Loan types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            
            -- Phase-I: Fraud Features
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

            -- Phase-II: Risk Features
            annual_income REAL,
            dti_ratio REAL,
            total_emi REAL,
            payment_stress REAL,
            num_loans INTEGER,
            monthly_balance REAL,
            age INTEGER,

            -- Assignment & Metadata
            assigned_to TEXT,
            status TEXT DEFAULT 'Pending',
            system_decision TEXT,
            analyst_decision TEXT,
            comments TEXT,
            case_type TEXT -- 'Fraud' or 'Loan'
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()