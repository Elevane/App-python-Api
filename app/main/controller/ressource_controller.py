from flask import request
from flask_restplus import Resource

from ..utils.dto import RessourceDto
from ..service.ressource_service import save_new_ressource, get_all_ressource, get_a_ressource, update_ressource

api = RessourceDto.api
_ressource = RessourceDto.ressource


@api.route('/')
class Ressource(Resource):
    @api.doc('list_of_ressources')
    @api.marshal_list_with(_ressource, envelope='data')
    def get(self):
        return get_all_ressource()

    @api.response(201, 'ressource successfully created.')
    @api.doc('create a new ressource')
    @api.expect(_ressource, validate=True)
    def post(self):
        data = request.json
        return save_new_ressource(data=data)

    @api.response(201, 'ressource successfully updated.')
    @api.doc('update a ressource')
    @api.expect(_ressource, validate=True)
    def put(self):
        data = request.json
        ressource = get_a_ressource(data['id'])
        if not ressource:
            api.abort(404)
        else:
            return update_ressource(data)


@api.route('/<id>')
@api.param('id', 'The ressource identifier')
@api.response(404, 'ressource not found.')
class Ressource(Resource):
    @api.doc('get a ressource')
    @api.marshal_with(_ressource)
    def get(self, id):
        ressource = get_a_ressource(id)
        if not ressource:
            api.abort(404)
        else:
            return ressource

