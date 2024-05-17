# Controller definitions for user auth and profiles

from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import auth_service
from .models import LoginUserSchema, RegisterUserSchema

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@bp.post('/register')
def register():
    """
    Register user
    ---
    tags:
        -   auth
    parameters:
        -   name: user
            in: body
            required: true
            schema:
                properties:
                    username:
                        type: string
                        description: Username.
                        example: cool_user
                    email:
                        type: string
                        description: Email of user.
                        example: coolman@all.time
                    password:
                        type: string
                        description: Password of user.
                        example: cool_p@ssw0rd
    responses:
        200:
            description: Task updated
            examples:
                application/json: {"message": "User registered successfully"}
        400:
            description: Bad request
            examples:
                application/json: {"message": "Bad request"}
    """

    # Get the request data
    data = request.get_json()
    register_user_schema = RegisterUserSchema()
    errors = register_user_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    return auth_service.register_user(data)


@bp.post('/login')
def login():
    """
    Login user
    ---
    tags:
        -   auth
    parameters:
        -   name: user
            in: body
            required: true
            schema:
                properties:
                    username:
                        type: string
                        description: Username.
                        example: cool_user
                    password:
                        type: string
                        description: Password of user.
                        example: cool_p@ssw0rd
    responses:
        200:
            description: User login successful
            examples:
                application/json: {"access_token": "secure_access_token"}
        401:
            description: Unauthorized
            examples:
                application/json: {"message": "Invalid username or password"}
    """

    # Get the request data
    data = request.get_json()
    login_user_schema = LoginUserSchema()
    errors = login_user_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    return auth_service.login_user(data)


@bp.get('/profile')
@jwt_required()
def get_user_profile():
    """
    Load user profile
    ---
    tags:
        -   auth
    parameters:
        -   name: Authorization
            in: header
            required: true
            type: string
    responses:
        200:
            description: Task updated
            examples:
                application/json: {"message": "User found", "data": {"username": "cool_user"}}
        404:
            description: Not found
            examples:
                application/json: {"message": "Not found"}
    """

    # Get the current user ID from the access token
    user_id = get_jwt_identity()

    return auth_service.get_user_profile(user_id)
