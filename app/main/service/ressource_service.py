import uuid
from datetime import datetime

from app.main import db
from app.main.model.ressource import Ressource


def save_new_ressource(data):
    ressource = Ressource.query.filter_by(name=data['name']).first()
    if not ressource:
        new_ressource = Ressource(
            quantity=data['quantity'],
            name=data['name'],
            unity=data['unity'],
        )
        save_changes(new_ressource)
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


def get_all_ressource():
    return Ressource.query.all()


def get_a_ressource(ressource_id):
    return Ressource.query.filter_by(id=ressource_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_ressource(ressource_id):
    res = Ressource.query.get(ressource_id)
    db.session.delete(res)
    db.session.commit()


def update_ressource(data):
    ressource = Ressource.query.get(data['id'])
    if ressource:
        ressource.name = data['name']
        ressource.quantity = data['quantity']
        ressource.unity = data['unity']

        save_changes(ressource)
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

