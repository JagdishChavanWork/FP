import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(input_password, stored_password):
    """
    input_password: str
    stored_password: bytes (from DB)
    """

    try:
        return bcrypt.checkpw(
            input_password.encode('utf-8'),
            stored_password
        )
    except Exception as e:
        print("Password check error:", e)
        return False