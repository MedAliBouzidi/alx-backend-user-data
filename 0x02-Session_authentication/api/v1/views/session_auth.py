#!/usr/bin/env python3
""" Session Authentication View """
from os import getenv

from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    POST /auth_session/login
        Return:
          - User object JSON representation
    """
    email = request.form.get("email")
    if email is None or email == "":
        return {"error": "email missing"}, 400
    password = request.form.get("password")
    if password is None or password == "":
        return {"error": "password missing"}, 400
    user = User.search({"email": email})
    user = user[0] if user else None
    if user is None:
        return {"error": "no user found for this email"}, 404
    if not user.is_valid_password(password):
        return {"error": "wrong password"}, 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response

@app_views.route("/auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout():
    """ Logout from Sesson """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
