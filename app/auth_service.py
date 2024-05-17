# business logic for the authentication/profile service
from typing import Tuple

from flask import jsonify, Response
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User
from flask_jwt_extended import create_access_token


def register_user(data: dict) -> Tuple[Response, int]:
    # Extract the username and password from the data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the username already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Username/email already exists'}), 400

    # Create a new user object
    user = User(username=username, email=email, password=generate_password_hash(password))

    # Add the user to the database
    user.save()

    return jsonify({'message': 'User registered successfully'}), 201


def login_user(data: dict) -> Tuple[Response, int]:
    # Extract the username and password from the data
    username = data.get('username')
    password = data.get('password')

    # Find the user in the database
    user: User = User.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password, password):

        # Generate the access token
        access_token = create_access_token(identity=user.id)

        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid username or password'}), 401


def get_user_profile(user_id: int) -> Tuple[Response, int]:
    # get user details by ID
    user: User = db.get_or_404(User, user_id)

    return jsonify({'message': 'User found', 'data': user.serialize()}), 200
