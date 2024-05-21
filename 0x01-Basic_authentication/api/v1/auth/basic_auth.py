#!/usr/bin/env python3
""" Basic Auth module """
import base64
from os import walk
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Auth class"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extract the base64 authorization header"""
        if (
            authorization_header is None
            or isinstance(authorization_header, str) is False
            or authorization_header.startswith("Basic ") is False
        ):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode the base64 authorization header"""
        if (
            base64_authorization_header is None
            or isinstance(base64_authorization_header, str) is False
        ):
            return None
        try:
            decoded = base64.b64decode(
                base64_authorization_header.encode("utf-8")
            )
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract the user credentials"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return None, None
        splitted = decoded_base64_authorization_header.split(":")
        return (splitted[0], splitted[1])

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """User object from credentials"""
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None
