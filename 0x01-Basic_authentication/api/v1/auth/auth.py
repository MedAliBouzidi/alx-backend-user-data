#!/usr/bin/env python3
""" Auth module for the API """
from typing import TypeVar

from flask import request


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth method
        Returns:
          - True if the path is not in the list of strings excluded_paths
          - False otherwise
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        authorization_header method
        Returns:
          - None if request does not contain the header key 'Authorization'
          - the value of the header
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        current_user method
        Returns:
          - None if the request is not authorized
          - the value of the request header Authorization
        """
        return None
