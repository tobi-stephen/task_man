# Controller definitions for managing tasks

from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import task_service
from .models import TaskSchema

bp = Blueprint('tasks', __name__, url_prefix='/api/v1/tasks')


@bp.post('')
@jwt_required()
def create_task():
    """
    Create task
    ---
    tags:
        - tasks
    parameters:
        -   name: Authorization
            in: header
            required: true
            type: string
        -   name: task
            in: body
            required: true
            schema:
                properties:
                    title:
                        type: string
                        description: Title of the task.
                        example: Be a millionaire
                    description:
                        type: string
                        description: Description of the task.
                        example: Work hard, pray hard, work harder
    responses:
        201:
            description: Task created
            examples:
                application/json: {"message": "Task created", "data": {"title": "Title", "description": "Description", "user_id": 1}}
        400:
            description: Bad request
            examples:
                application/json: {"message": "Bad request"}
    """

    # Get the current user ID from the access token
    user_id = get_jwt_identity()

    # Get the request data
    data = request.get_json()

    task_schema = TaskSchema()
    errors = task_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    return task_service.create_task(user_id, data)


@bp.get('')
@jwt_required()
def get_all_tasks():
    """
    Get all tasks by user
    ---
    tags:
        - tasks
    parameters:
        -   name: Authorization
            in: header
            required: true
            type: string
    responses:
        200:
            description: Tasks fetch successful
            examples:
                application/json: {"message": "Success", "data": [{"title": "Title", "description": "Description", "user_id": 1}]}
        404:
            description: Task not found
            examples:
                application/json: {"message": "Task not found"}
    """

    # Get the current user ID from the access token
    user_id = get_jwt_identity()

    return task_service.get_all_tasks(user_id)


@bp.get('/<int:task_id>')
@jwt_required()
def get_task(task_id: int):
    """
    Get task by ID
    ---
    tags:
        - tasks
    parameters:
        -   name: Authorization
            in: header
            required: true
            type: string
        -   name: task_id
            in: path
            required: true
            type: integer
    responses:
        200:
            description: Task found
            examples:
                application/json: {"message": "Task found", "data": {"title": "Title", "description": "Description", "user_id": 1}}
        404:
            description: Task not found
            examples:
                application/json: {"message": "Task not found"}
    """

    # Get the current user ID from the access token
    user_id = get_jwt_identity()

    return task_service.get_task(user_id, task_id)


@bp.put('/<int:task_id>')
@jwt_required()
def update_task(task_id):
    """
    Update task
    ---
    tags:
        - tasks
    parameters:
        -   name: Authorization
            in: header
            required: true
            type: string
        -   name: task_id
            in: path
            required: true
            type: integer
        -   name: task
            in: body
            required: true
            schema:
                properties:
                    title:
                        type: string
                        description: Title of the task.
                        example: Be a millionaire
                    description:
                        type: string
                        description: Description of the task.
                        example: Work hard, pray hard, work harder
    responses:
        200:
            description: Task updated
            examples:
                application/json: {"message": "Success", "data": {"title": "Title", "description": "Description", "user_id": 1}}
        404:
            description: Task not found
            examples:
                application/json: {"message": "Task not found"}
    """

    # Get the current user ID from the access token
    user_id = get_jwt_identity()

    # Get the request data
    data = request.get_json()

    task_schema = TaskSchema()
    errors = task_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    return task_service.update_task(user_id, task_id, data)


@bp.delete('/<int:task_id>')
@jwt_required()
def delete_task(task_id):
    """
    Delete task
    ---
    tags:
        - tasks
    parameters:
        -   name: Authorization
            in: header
            required: true
            type: string
        -   name: task_id
            in: path
            required: true
            type: integer
    responses:
        204:
            description: Task removed
        404:
            description: Task not found
            examples:
                application/json: {"message": "Task not found"}
    """

    # Get the current user ID from the access token
    user_id = get_jwt_identity()

    return task_service.delete_task(user_id, task_id)
