# Project Name

A tasks management application with streaming support.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## Description

This project is a tasks management REST API that allows users to manage tasks. It includes streaming via socket connection and user authentication service using JWT.

## Features

- Task creation, editing, and deletion
- Real-time streaming of task updates
- User authentication and authorization
- User profile management - view

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/tobi-stephen/task_man.git
    ```

2. Install the dependencies:

    ```sh
    cd task_man
    python -m venv . # creates a virtual env
    pip install -r requirements.txt # install all py dependencies
    ```

3. Start the application:

    ```sh
    python run.py
    ```

## Usage

- http://localhost:5000/apidocs/ (Swagger docs)

1. Register a new user account.
2. log in with an existing account. (This will generate an access token which can be used in further operations)
3. User creates task
4. Update task details as needed.
5. Manage user profile.


## Technologies

- Backend: Python, Flask
- Database: SQLite
- Authentication: JWT
- Real-time Streaming: Flask-SocketIO

## Streaming test

In order to stream tasks updates by a specific, a test html route is available at [http://localhost:5000/tasks?<access_token>]
Where <access_token> is the token generated from the login API route

- Create new tasks, update an existing one and delete tasks using the API and the web page will automatically be updated
- Note that the individual task detail is a simple model binded to the logged in user.
