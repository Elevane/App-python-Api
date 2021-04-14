from flask import request
from flask_restplus import Resource

from ..utils.dto import MessageDto
from ..service.message_service import save_new_message, get_all_message, get_a_message, update_message

api = MessageDto.api
_message = MessageDto.message


@api.route('/')
class MessageList(Resource):
    @api.doc('list_of_message')
    @api.marshal_list_with(_message, envelope='data')
    def get(self):
        return get_all_message()

    @api.response(201, 'Message successfully created.')
    @api.doc('create a new message')
    @api.expect(_message, validate=True)
    def post(self):
        data = request.json
        return save_new_message(data=data)

    @api.response(201, 'Message successfully updated.')
    @api.doc('update a message')
    @api.expect(_message, validate=True)
    def put(self):
        data = request.json
        message = get_a_message(data['id'])
        if not message:
            api.abort(404)
        else:
            return update_message(data)


@api.route('/<id>')
@api.param('id', 'The message identifier')
@api.response(404, 'message not found.')
class Message(Resource):
    @api.doc('get a message')
    @api.marshal_with(_message)
    def get(self, id):
        message = get_a_message(id)
        if not message:
            api.abort(404)
        else:
            return message

