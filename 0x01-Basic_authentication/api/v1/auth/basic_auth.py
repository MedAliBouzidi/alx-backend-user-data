#!/usr/bin/env python3
""" Basic Auth module """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extract the base64 authorization header"""
        if (
            authorization_header is None
            or isinstance(authorization_header, str) is False
            or authorization_header.startswith("Basic ") is False
        ):
            return None
        return authorization_header[6:]
