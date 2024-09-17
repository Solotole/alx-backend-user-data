#!/usr/bin/env python3
"""basic authentication class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """autentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method
        """
        return False
    
    def authorization_header(self, request=None) -> str:
        """suthorization method handler
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """retriving current user
        """
        return None
