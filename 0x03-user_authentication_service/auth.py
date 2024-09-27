#!/usr/bin/env python3
"""hashing a password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hashing a password and return bytes of
    password
    """
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(bytes_password, salt)
    return hash_password


def _generate_uuid() -> str:
    """generating a unique id using uuid module and returning it
    """
    unique: str = str(uuid4())
    return unique


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

    def valid_login(self, email: str, password: str) -> bool:
        """finding a user by email"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email):
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None
        # return None
        # user = self._db.get(email)
        # if user:
        # ession_id = self._generate_uuid()
        # self._db[email]['session_id'] = session_id
        # return session_id
        # return None
