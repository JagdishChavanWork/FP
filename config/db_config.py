import sqlite3

def get_connection():
    return sqlite3.connect("database/db.sqlite3", check_same_thread=False)