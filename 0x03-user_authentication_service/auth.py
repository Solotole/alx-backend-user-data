#!/usr/bin/env python3
"""hashing a password
"""
import bcrypt


def _hash_password(password: str):
    """hashing a password and return bytes of
    password
    """
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(bytes_password, salt)
    return hash_password
