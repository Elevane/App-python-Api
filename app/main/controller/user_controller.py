from flask import request
from flask_restplus import Resource

from ..utils.dto import UserDto
from ..service.user_service import check_existing_user

api = UserDto.api
_user = UserDto.user


@api.route('/getuser')
@api.response(404, 'user not found.')
class Login(Resource):
    @api.response(201, 'User exist.')
    @api.doc('check if user exist')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.json
        return check_existing_user(email=data['email'], password=data['password'])

