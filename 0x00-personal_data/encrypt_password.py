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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.

    Args:
    hashed_password (bytes): The hashed password.
    password (str): The password to validate.

    Returns:
    bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
