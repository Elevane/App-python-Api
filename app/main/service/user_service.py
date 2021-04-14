import uuid
from datetime import datetime

from app.main import db
from app.main.model.user import User


def check_existing_user(email, password):
    exist = User.query.filter_by(email=email,password=password).first()

    if exist:
        response_object = {
            'status': 'success',
            'value' : True
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'Fail',
            'value': False
        }
        return response_object, 409



