#!/usr/bin/env python3
"""hashing a password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashing a password and return bytes of
    password
    """
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(bytes_password, salt)
    return hash_password

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """intitialization method
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and password
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
