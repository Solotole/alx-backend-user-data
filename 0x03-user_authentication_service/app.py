#!/usr/bin/env python3
"""Flask app development
"""
from flask import Flask, redirect, jsonify, request
from flask import abort
from auth import Auth

AUTH: Auth = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_route():
    """home router
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """registering a user if not existing
    and if otherwise acknowledges it
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """POST /sessions
    Handles user login by validating credentials and creating a session.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """function to delete a user id from a session
    """
    session = request.cookies.get('session_id')
    if not session:
        return abort(403)
    user = AUTH.get_user_from_session_id(session)
    if not user:
        return abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """profile function route
    """
    session = request.cookies.get('session_id')
    if not session:
        return abort(403)
    user = AUTH.get_user_from_session_id(session)
    if user:
        return jsonify({"email": user.email}), 200
    if not user:
        return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
