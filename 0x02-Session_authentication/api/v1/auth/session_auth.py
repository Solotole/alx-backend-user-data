#!/usr/bin/env python3
"""session auth class
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """session auth class definition
    """
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """creating a session"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retriving user's is of specific session id key from
        the class instance
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
