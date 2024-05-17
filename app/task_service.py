# business logic for the task management service
import datetime
from typing import Tuple

from flask import jsonify, Response

from werkzeug.exceptions import NotFound

from app import db
from app.models import Task


def create_task(user_id: int, data: dict) -> Tuple[Response, int]:
    # Extract the title and description from the data
    title = data.get('title')
    description = data.get('description')

    # Create a new Task object
    task = Task(title=title, description=description, user_id=user_id)

    # Add the task to the database
    task.save()

    return jsonify({'message': 'Task created', 'data': task.serialize()}), 201


def update_task(user_id: int, task_id: int, data: dict) -> Tuple[Response, int]:
    # Extract the title and description from the data
    title = data.get('title')
    description = data.get('description')

    # Find the task in the database
    task = db.session.execute(db.select(Task).filter_by(id=task_id, user_id=user_id)).scalar_one_or_none()
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    # Update the task details
    task.update(title=title, description=description)

    return jsonify({'message': 'Task updated', 'data': task.serialize()}), 201


def get_all_tasks(user_id: int) -> Tuple[Response, int]:
    # get all task details created by 'user_id' and paginated
    user_tasks = {}
    try:
        user_tasks = db.paginate(db.select(Task).filter_by(user_id=user_id).order_by(Task.id), max_per_page=10)
    except NotFound:
        pass

    result = [task.serialize() for task in user_tasks]

    return jsonify({'message': 'Success', 'data': result}), 200


def get_task(user_id: int, task_id: int) -> Tuple[Response, int]:
    # get task details by ID
    task = db.session.execute(db.select(Task).filter_by(id=task_id, user_id=user_id)).scalar_one_or_none()
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify({'message': 'Task found', 'data': task.serialize()}), 200


def delete_task(user_id: int, task_id: int) -> Tuple[Response, int]:
    # get task details by ID
    task = db.session.execute(db.select(Task).filter_by(id=task_id, user_id=user_id)).scalar_one_or_none()
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.delete()

    return jsonify({'message': 'Task removed'}), 204
