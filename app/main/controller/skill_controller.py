from flask import request
from flask_restplus import Resource

from ..utils.dto import SkillDto
from ..service.skill_service import save_new_skill, get_all_skill, get_a_skill, update_skill, delete_skill

api = SkillDto.api
_skill = SkillDto.skill


@api.route('/')
class Skill(Resource):
    @api.doc('list_of_skills')
    @api.marshal_list_with(_skill, envelope='data')
    def get(self):
        return get_all_skill()

    @api.response(201, 'skill successfully created.')
    @api.doc('create a new skill')
    @api.expect(_skill, validate=True)
    def post(self):
        data = request.json
        return save_new_skill(data=data)

    @api.response(201, 'skill successfully updated.')
    @api.doc('update a skill')
    @api.expect(_skill, validate=True)
    def patch(self):
        data = request.json
        skill = get_a_skill(data['id'])
        if not skill:
            api.abort(404)
        else:
            return update_skill(data)


@api.route('/<id>')
@api.param('id', 'The skill identifier')
@api.response(404, 'skill not found.')
class Skill(Resource):
    @api.doc('get a skill')
    @api.marshal_with(_skill)
    def get(self, id):
        skill = get_a_skill(id)
        if not skill:
            api.abort(404)
        else:
            return skill

    @api.doc('delete a skill')
    @api.marshal_with(_skill)
    def delete(self, id):
        skill = get_a_skill(id)
        if not skill:
            api.abort(404)
        else:
            delete_skill(skill)


