import sqlite3
import pandas as pd
import os
import datetime

DB_PATH = 'fraudpulse_system.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def initialize_database():
    """Creates tables and optimization indexes for high-speed retrieval."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Employee Management Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees 
        (id TEXT PRIMARY KEY, name TEXT, email TEXT, role TEXT, dept TEXT, status TEXT)''')
    
    # 2. Fraud Data Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS fraud_data 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, step INTEGER, type TEXT, amount REAL, 
         nameOrig TEXT, oldbalanceOrg REAL, newbalanceOrig REAL, nameDest TEXT, 
         isFraud INTEGER, isFlaggedFraud INTEGER)''')
    
    # 3. Credit Risk Data Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS risk_data 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, Age REAL, Annual_Income REAL, 
         Num_Bank_Accounts REAL, Num_Credit_Card REAL, Interest_Rate REAL, 
         Num_of_Loan REAL, Credit_Score TEXT, Risk_Score_Proxy REAL)''')

    # 4. Global Audit Table (Tracking solved cases)
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases_resolved 
        (case_id TEXT PRIMARY KEY, type TEXT, model_verdict TEXT, 
         analyst_verdict TEXT, comment TEXT, resolved_at DATETIME)''')

    # PERFORMANCE INDEXES
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fraud_type ON fraud_data(type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fraud_isfraud ON fraud_data(isFraud)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_risk_score ON risk_data(Credit_Score)")
    
    conn.commit()
    conn.close()

def migrate_csv_to_db(fraud_path, risk_path):
    """Ingests CSV data into SQLite only if the tables are empty."""
    conn = get_db_connection()
    if os.path.exists(fraud_path):
        db_count = pd.read_sql_query("SELECT count(*) as total FROM fraud_data", conn).iloc[0]['total']
        if db_count == 0:
            for chunk in pd.read_csv(fraud_path, chunksize=10000):
                cols = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 
                        'newbalanceOrig', 'nameDest', 'isFraud', 'isFlaggedFraud']
                chunk[cols].to_sql('fraud_data', conn, if_exists='append', index=False)

    if os.path.exists(risk_path):
        db_count = pd.read_sql_query("SELECT count(*) as total FROM risk_data", conn).iloc[0]['total']
        if db_count == 0:
            for chunk in pd.read_csv(risk_path, chunksize=10000):
                cols = ['Age', 'Annual_Income', 'Num_Bank_Accounts', 'Num_Credit_Card', 
                        'Interest_Rate', 'Num_of_Loan', 'Credit_Score', 'Risk_Score_Proxy']
                chunk[cols].to_sql('risk_data', conn, if_exists='append', index=False)
            
    conn.commit()
    conn.close()

def execute_custom_query(query):
    """Safely executes a custom SQL query and returns a DataFrame."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Query Error: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def save_analyst_verdict(case_id, case_type, model_verdict, analyst_verdict, comment):
    """
    Saves the analyst's decision to the database to track completed tasks.
    Used to update the 'Tasks Completed' counters.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # We use INSERT OR REPLACE so if an analyst updates a comment, it updates the same row
        cursor.execute('''
            INSERT OR REPLACE INTO cases_resolved 
            (case_id, type, model_verdict, analyst_verdict, comment, resolved_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (f"TXN-{case_id}", case_type, model_verdict, analyst_verdict, comment, now))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Database Save Error: {e}")
        return False
    finally:
        conn.close()