#!/usr/bin/env python3
""" Auth module for the API """
import re
from typing import List, TypeVar

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
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        # for path_excluded in excluded_paths:
        #     if (
        #         path_excluded.startswith(path)
        #         or path.startswith(path_excluded)
        #         or (
        #             path_excluded[-1] == "*"
        #             and path.startswith(path_excluded[:-1])
        #         )
        #     ):
        #         return False
        for path_excluded in excluded_paths:
            if path_excluded.startswith(path):
                return False
            if path.startswith(path_excluded):
                return False
            if path_excluded[-1] == "*":
                if path.startswith(path_excluded[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header method
        Returns:
          - None if request does not contain the header key 'Authorization'
          - the value of the header
        """
        if request is None or request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """
        current_user method
        Returns:
          - None if the request is not authorized
          - the value of the request header Authorization
        """
        return None
