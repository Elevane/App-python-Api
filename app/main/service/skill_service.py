import uuid
from datetime import datetime

from app.main import db
from app.main.model.skill import Skill
from app.main.utils.SessionManager import save_changes, delete

def save_new_skill(data):
    skill = Skill.query.filter_by(name=data['name']).first()
    
    if not skill:
        new_skill = Skill(
            ratio=data['ratio'],
            name=data['name'],
            active=data['active'],
        )
        save_changes(new_skill)
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



def get_all_skill():
    skill = Skill.query.all()
    if skill:
        return skill
    else:
        response_object = {
            'status': 'Error',
            'message': 'Error while trying to get ressources',
        }
        return response_object, 409


def get_a_skill(skill_id):
    return Skill.query.filter_by(id=skill_id).first()





def delete_skill(skill):

    if skill:
        delete(skill)
        response_object = {
            'status': 'success',
            'message': 'Successfully deleted.'
        }
        return response_object
    else:
        response_object = {
            'status': 'error',
            'message': 'failed deleted.'
        }
        return response_object


def update_skill(data):
    skill = Skill.query.get(data['id'])

    if skill:
        skill.name = data['name']
        skill.ratio = data['ratio']
        skill.active = data['active']

        save_changes(skill)
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

