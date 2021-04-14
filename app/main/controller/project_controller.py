from flask import request
from flask_restplus import Resource

from ..utils.dto import ProjectDto
from ..service.project_service import save_new_project, get_all_projects, get_a_project, update_project

api = ProjectDto.api
_project = ProjectDto.project


@api.route('/')
class ProjectList(Resource):
    @api.doc('list_of_projects')
    @api.marshal_list_with(_project, envelope='data')
    def get(self):
        return get_all_projects()

    @api.response(201, 'Project successfully created.')
    @api.doc('create a new project')
    @api.expect(_project, validate=True)
    def post(self):
        data = request.json
        return save_new_project(data=data)

    @api.response(201, 'Project successfully updated.')
    @api.doc('update a project')
    @api.expect(_project, validate=True)
    def put(self):
        data = request.json
        project = get_a_project(data['id'])
        if not project:
            api.abort(404)
        else:
            return update_project(data)


@api.route('/<id>')
@api.param('id', 'The Project identifier')
@api.response(404, 'Project not found.')
class Project(Resource):
    @api.doc('get a project')
    @api.marshal_with(_project)
    def get(self, id):
        project = get_a_project(id)
        if not project:
            api.abort(404)
        else:
            return project

