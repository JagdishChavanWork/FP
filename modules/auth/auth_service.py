import sqlite3
from utils.security import check_password


def login_user(email, password):

    email = email.lower().strip()

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password, role, position FROM users WHERE email=?",
        (email,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password, role, position = result

        print("INPUT PASSWORD:", password)
        print("STORED HASH:", stored_password)

        if check_password(password, stored_password):
            print("PASSWORD MATCH")
            return role, position
        else:
            print("PASSWORD MISMATCH")

    return None, None