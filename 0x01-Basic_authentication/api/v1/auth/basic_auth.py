#!/usr/bin/env python3
""" Basic Auth module """
import base64

from api.v1.auth.auth import Auth


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
        """Decode the base64 authorization header """
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
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
        splitted = decoded_base64_authorization_header.split(':')
        return (splitted[0], splitted[1])
