from app import socketio


# routine to emit single task event to user's room
def emit_task(event: str, task, user_id: int):
    socketio.emit(event, task.serialize(), room=str(user_id))
    