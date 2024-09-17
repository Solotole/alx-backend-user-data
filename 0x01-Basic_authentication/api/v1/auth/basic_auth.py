#!/usr/bin/env python3
"""another basic auth class"""
from api.v1.auth.auth import Auth
import base64
import binascii


class BasicAuth(Auth):
    """child class to the Auth class
    """
    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """extracting value of the base64 header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if (authorization_header.startswith('Basic') and
                authorization_header[5] == ' '):
            return authorization_header[6:]
        if (authorization_header.startswith('Basic') and
                authorization_header[5] != ' '):
            return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            data = base64.b64decode(base64_authorization_header, validate=True)
            return data.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """extracting users credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        index = decoded_base64_authorization_header.find(':')
        first = decoded_base64_authorization_header[0:index]
        second = decoded_base64_authorization_header[index + 1:]
        return (first, second)
