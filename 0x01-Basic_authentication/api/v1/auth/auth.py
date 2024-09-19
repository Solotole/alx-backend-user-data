#!/usr/bin/env python3
"""basic authentication class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """autentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method
        """
        if path is None:
            return True
        if (
            (excluded_paths is not None and len(excluded_paths) == 0) or
            excluded_paths is None
        ):
            return True
        if path in excluded_paths:
            return False
        if path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """suthorization method handler
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retriving current user
        """
        return None
