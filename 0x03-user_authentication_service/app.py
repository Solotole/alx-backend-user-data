#!/usr/bin/env python3
"""Flask app development
"""
from flask import Flask, jsonify, request
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
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
