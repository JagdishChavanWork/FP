import sqlite3

def authenticate_user(email, password):
    """Checks the database for a matching email and password."""
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    
    # We query the database for the specific email and password
    cursor.execute("SELECT id, email, role, position FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        # Returns a dictionary of user data if found
        return {
            "id": user[0],
            "email": user[1],
            "role": user[2],
            "position": user[3]
        }
    return None