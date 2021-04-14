from flask_restplus import Namespace, fields


class ProjectDto:
    api = Namespace('project', description='project related operations')
    project = api.model('project', {
        'name': fields.String(required=True, description='project\'s name'),
        'image': fields.String(required=True, description='project\'s image'),
        'description': fields.String(required=True, description='project\'s description'),
        'skills': fields.String(required=True, description='project\'s skill'),
        'id': fields.String(description='project\'s id')
    })


class BlogDto:
    api = Namespace('blog', description='blog related operations')
    blog = api.model('blog', {
        'title': fields.String(required=True, description='blog title'),
        'date': fields.Date(required=True, description='blog date'),
        'image': fields.String(required=True, description='blog image path'),
        'text': fields.String(required=True, description='blog text'),
        'id': fields.String(description='blog id')
    })


class MessageDto:
    api = Namespace('message', description='message related operations')
    message = api.model('message', {
        'title': fields.String(required=True),
        'name': fields.String(required=True),
        'message': fields.String(required=True),
        'email': fields.String(required=True),
        'id': fields.String(description='blog id')
    })


class RessourceDto:
    api = Namespace('ressource', description='ressource related operations')
    ressource = api.model('ressource', {
        'quantity': fields.String(required=True),
        'name': fields.String(required=True),
        'unity': fields.String(required=True),
        'id': fields.String(description='blog id')
    })


class SkillDto:
    api = Namespace('skill', description='skill related operations')
    skill = api.model('skill', {
        'name': fields.String(required=True),
        'ratio': fields.String(required=True),
        'active': fields.Boolean(required=True),
        'id': fields.String(description='blog id')
    })










