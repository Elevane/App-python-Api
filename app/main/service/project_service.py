import uuid
import datetime

from app.main import db
from app.main.model.project import Project
from app.main.utils.SessionManager import save_changes, delete

def save_new_project(data):
    project = Project.query.filter_by(name=data['name']).first()
    if not project:
        new_project = Project(
            name=data['name'],
            image=data['image'],
            description=data['description'],
            skills=data['skills'],
        )
        save_changes(new_project)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Project already exists',
        }
        return response_object, 409


def get_all_projects():
    return Project.query.all()


def get_a_project(project_id):
    return Project.query.filter_by(id=project_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def delete_project(project_id):
    res = Project.query.get(project_id)
    if res:
       delete(res)


def update_project(data):
    project = Project.query.get(data['id'])
    if project:
        project.name = data['name']
        project.image = data['image']
        project.description = data['description']
        project.skills = data['skills']
        save_changes(project)
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