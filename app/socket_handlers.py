# This routine is used to handle socket connections

from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from werkzeug.exceptions import NotFound

from app import db, logger
from app.models import Task, User
from app import socketio


# Local registry of connected users
# can be used to broadcast messages to all connected users
connected_users = {}


@socketio.on('connect')
def handle_connect():
    try:
        verify_jwt_in_request(locations='query_string')
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            raise Exception('User not found')
        
        join_room(str(user_id))
        connected_users[user_id] = request.sid
        logger.info("Client connected")
    except Exception as e:
        logger.error('Error during connect:', str(e))
        emit('unauthorized', {'message': 'Invalid token'})
        disconnect()


@socketio.on('disconnect')
def handle_disconnect():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        leave_room(str(user_id))
        connected_users.pop(user_id)
        logger.info('Client disconnected')
    except Exception as e:
        logger.error('Error during disconnect:', str(e))


@socketio.on('get_tasks')
def emit_tasks():
    verify_jwt_in_request(locations='query_string')
    user_id = get_jwt_identity()

    user_tasks = {}
    try:
        user_tasks = db.paginate(db.select(Task).filter_by(user_id=user_id).order_by(Task.id), max_per_page=4)
    except NotFound:
        pass

    logger.info(f"User {user_id} requested tasks")
    result = [task.serialize() for task in user_tasks]
    emit('tasks', result, room=str(user_id))
