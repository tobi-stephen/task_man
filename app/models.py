from datetime import datetime
from app import db
from app.socket_events import emit_task

from marshmallow import fields, Schema, validate


# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        db.session.commit()


# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'date_created': str(self.date_created),
            'date_modified': str(self.date_modified)
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        emit_task('task_created', self, self.user_id)

    def update(self, title, description):
        self.title = title
        self.description = description
        self.date_modified = datetime.now()
        db.session.commit()
        emit_task('task_updated', self, self.user_id)

    def delete(self):
        user_id = self.user_id # saving `user_id` for the socket event later before deleting the task

        db.session.delete(self)
        db.session.commit()
        emit_task('task_removed', self, user_id)


# Schema definitions for validating request
class RegisterUserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=6, max=30))
    email = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6, max=30))


class LoginUserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TaskSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=10))
