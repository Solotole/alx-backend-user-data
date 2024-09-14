#!/usr/bin/env python3
"""User passwords should NEVER be stored
in plain text in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a randomly generated salt using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted and hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
