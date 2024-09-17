#!/usr/bin/env python3
"""another basic auth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """child class to the Auth class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extracting value of the base64 header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic') and authorization_header[5] == ' ':
            return authorization_header[6:]
        if authorization_header.startswith('Basic') and authorization_header[5] != ' ':
            return None
        # return authorization_header[6:]
