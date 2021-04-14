import uuid
from datetime import datetime

from app.main import db
from app.main.model.skill import Skill


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
    return Skill.query.all()


def get_a_skill(skill_id):
    return Skill.query.filter_by(id=skill_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_skill(skill_id):
    res = Skill.query.get(skill_id)
    db.session.delete(res)
    db.session.commit()


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

