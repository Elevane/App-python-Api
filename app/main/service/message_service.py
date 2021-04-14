import uuid
from datetime import datetime

from app.main import db
from app.main.model.message import Message


def save_new_message(data):
    message = Message.query.filter_by(title=data['title']).first()
    if not message:
        new_message = Message(
            title=data['title'],
            name=data['name'],
            message=data['message'],
            email=data['email'],
        )
        save_changes(new_message)
        response_object = {
            'status': 'success',
            'message': 'Successfully created.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Object already exists',
        }
        return response_object, 409


def get_all_message():
    return Message.query.all()


def get_a_message(message_id):
    return Message.query.filter_by(id=message_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_message(blog_id):
    res = Message.query.get(blog_id)
    db.session.delete(res)
    db.session.commit()


def update_message(data):
    message = Message.query.get(data['id'])
    if message:
        message.title = data['title']
        message.name = data['name']
        message.message = data['message']
        message.email = data['email']
        save_changes(message)
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.'
        }
        return response_object, 201

    else:
        response_object = {
            'status' : 'fail',
            'message' : 'Object doesn\'t exist'
        }

        return response_object, 409


def process_date(date):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return datetime(year, month, day)