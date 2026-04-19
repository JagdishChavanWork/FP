import sqlite3
from services.time_service import get_current_timestamp, calculate_duration


DB_PATH = "database/db.sqlite3"


def mark_case_created(case_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    created_at = get_current_timestamp()

    cursor.execute("""
        UPDATE cases
        SET created_at = ?
        WHERE id = ?
    """, (created_at, case_id))

    conn.commit()
    conn.close()


def mark_case_completed(case_id, system_prediction, analyst_decision, comments):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    completed_at = get_current_timestamp()

    # Fetch created time
    cursor.execute("SELECT created_at FROM cases WHERE id = ?", (case_id,))
    created_at = cursor.fetchone()[0]

    duration = None
    if created_at:
        duration = calculate_duration(created_at, completed_at)

    cursor.execute("""
        UPDATE cases
        SET 
            system_prediction = ?,
            analyst_decision = ?,
            analyst_comments = ?,
            status = 'Completed',
            completed_at = ?,
            duration_seconds = ?
        WHERE id = ?
    """, (
        system_prediction,
        analyst_decision,
        comments,
        completed_at,
        duration,
        case_id
    ))

    conn.commit()
    conn.close()