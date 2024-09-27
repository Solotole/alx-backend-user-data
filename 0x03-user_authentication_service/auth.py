#!/usr/bin/env python3
"""hashing a password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


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

    def create_session(self, email: str) -> Union[str, None]:
        """creating a session"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find user by session ID.
        Args:
            session_id: string session ID.
        Returns:
            User object if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """method to destroy a session
        """
        if not user_id:
            return
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except Exception:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        unique: str = _generate_uuid()
        self._db.update_user(user.id, reset_token=unique)
        return unique

    def update_password(reset_token: str, password: str) -> None:
        """Update password and making reset_token None"""
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError
        hashed = _hash_password(password)
        user['hashed_password'] = hashed
        user['reset_token'] = None
        return None
