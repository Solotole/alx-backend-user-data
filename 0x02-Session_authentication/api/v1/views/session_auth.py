#!/usr/bin/env python3
"""Session authentication views
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from os import getenv
from api.v1.app import auth

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """POST /auth_session/login
    Handles the session login for users.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user_list = User.search({'email': email})
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404

    user = user_list[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    user_data = user.to_json()
    response = jsonify(user_data)
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
