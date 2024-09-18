#!/usr/bin/env python3
"""another basic auth class"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts user email and password from the Base64 decoded string.

    Args:
        decoded_base64_authorization_header (str): Decoded Base64 string in the format "email:password".

    Returns:
        Tuple[str, str]: A tuple of (email, password) if the format is correct, otherwise (None, None).
    """
    if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
        return None, None
    split_credentials = decoded_base64_authorization_header.split(':', 1)
    if len(split_credentials) != 2:
        return None, None

    user_email, user_pwd = split_credentials[0], split_credentials[1]
    
    return user_email, user_pwd

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """returns the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User.search({"email": user_email})
        if not users or len(users) == 0:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
            )
        if base64_auth_header is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(
            base64_auth_header
            )
        if decoded_auth is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
