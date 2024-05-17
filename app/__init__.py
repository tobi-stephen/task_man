# Entry point to the application
import json
import datetime
import logging

from flask import Flask, jsonify, render_template

from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from werkzeug.exceptions import HTTPException
    

# Create Flask app
app = Flask(__name__)

# Setup the socket connection
socketio = SocketIO(app)

# Configure logging
logger = logging.getLogger(name='TaskManagement')
logging.basicConfig(level=logging.ERROR)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models so that it can be captured by the create_db call
from .models import Task
from .models import User

# Configure Swagger for API documentation
template = {
    'swagger': '2.0',
    'info': {
        'title': 'Task Management API',
        'description': 'Task Management API docs.',
        'version': '1.0'
    }
}
swagger = Swagger(app, template=template)

# Setup the JWT for auth
app.config['JWT_SECRET_KEY'] = 'task_management_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=2)
app.config['JWT_QUERY_STRING_NAME'] = 'token'
jwt = JWTManager(app)

# route blueprints
from . import auth_controllers as auth
from . import task_controllers as tasks

# Configure blueprint controllers for API routes
app.register_blueprint(auth.bp)
app.register_blueprint(tasks.bp)

# Import socket handlers so it can be captured by the socketio call
from . import socket_handlers


# Additional routes
# Define a test route for streaming the task data
@app.get('/tasks')
def tasks_index():
    return render_template('index.html')

# Define a test route for health status
@app.get('/health')
def health():
    """
    Health status
    ---
    tags:
        -   health
    responses:
        200:
            description: OK Status
            examples:
                application/json: {"message": "OK"}
        400:
            description: Server error
            examples:
                application/json: {"message": "Server error"}
    """

    return jsonify({'message': 'OK'})


# Generic error handling
@app.errorhandler(Exception)
def handle_exceptions(e: Exception):
    logger.error(e)

    # Return server error for all other errors
    return jsonify({'status': 'Server error'}), 500


# Http error handling
@app.errorhandler(HTTPException)
def handle_http_exceptions(e: HTTPException):
    # Process HTTP errors into JSON response
    response = e.get_response()
    response.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description,
    })
    response.content_type = 'application/json'

    return response
