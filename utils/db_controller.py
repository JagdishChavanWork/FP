import sqlite3
import pandas as pd
import os

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
    
    # 2. Fraud Data Table (Optimized with specific types)
    cursor.execute('''CREATE TABLE IF NOT EXISTS fraud_data 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, step INTEGER, type TEXT, amount REAL, 
         nameOrig TEXT, oldbalanceOrg REAL, newbalanceOrig REAL, nameDest TEXT, 
         isFraud INTEGER, isFlaggedFraud INTEGER)''')
    
    # 3. Credit Risk Data Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS risk_data 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, Age REAL, Annual_Income REAL, 
         Num_Bank_Accounts REAL, Num_Credit_Card REAL, Interest_Rate REAL, 
         Num_of_Loan REAL, Credit_Score TEXT, Risk_Score_Proxy REAL)''')

    # 4. Global Audit Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases_resolved 
        (case_id TEXT PRIMARY KEY, type TEXT, model_verdict TEXT, 
         analyst_verdict TEXT, comment TEXT, resolved_at DATETIME)''')

    # --- PERFORMANCE INDEXES (The 'Search Shortcut' for SQL) ---
    # These prevent the "Screen Stuck" issue by allowing instant filtering
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fraud_type ON fraud_data(type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fraud_isfraud ON fraud_data(isFraud)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_risk_score ON risk_data(Credit_Score)")
    
    conn.commit()
    conn.close()

def migrate_csv_to_db(fraud_path, risk_path):
    """
    Ingests CSV data into SQLite only if the tables are empty.
    This ensures 'Incremental Growth' without duplicating existing data.
    """
    conn = get_db_connection()
    
    # --- Process Fraud Dataset ---
    if os.path.exists(fraud_path):
        db_count = pd.read_sql_query("SELECT count(*) as total FROM fraud_data", conn).iloc[0]['total']
        if db_count == 0:
            # We use chunksize to prevent memory crashes during large file ingestion
            for chunk in pd.read_csv(fraud_path, chunksize=10000):
                # Clean columns to match our schema exactly
                cols = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 
                        'newbalanceOrig', 'nameDest', 'isFraud', 'isFlaggedFraud']
                chunk[cols].to_sql('fraud_data', conn, if_exists='append', index=False)

    # --- Process Risk Dataset ---
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
    finally:
        conn.close()