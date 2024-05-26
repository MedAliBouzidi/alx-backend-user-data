#!/usr/bin/env python3
""" Session Database Authentication Module """
from datetime import datetime, timedelta

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session Database Authentication Class """

    def create_session(self, user_id: str = None) -> str:
        """ Create a session ID """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        kwargs = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Get User from Session ID """
        if session_id is None:
            return None
        sessions = UserSession.search({"session_id": session_id})
        try:
            user_session = sessions[0]
        except Exception:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        time_after_creation = (datetime.utcnow() - user_session.created_at)
        if time_after_creation.seconds > self.session_duration:
            return None
        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroys an authenticated session """
        session_id = self.session_cookie(request)
        sessions = UserSession.search({'session_id': session_id})
        try:
            sessions[0].remove()
        except Exception:
            return False
        return True
