#!/usr/bin/env python3
""" Session Authentication Expiration Module """
from datetime import datetime
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Expiration Authentication Class """

    def __init__(self) -> None:
        """ Constructor """
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get User from Session ID """
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_id is None or session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if "created_at" not in session_dict:
            return None
        time_after_creation = (datetime.now() - session_dict.get("created_at"))
        if time_after_creation.seconds > self.session_duration:
            return None
        return session_dict.get("user_id")
