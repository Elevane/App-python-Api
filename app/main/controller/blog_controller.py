from flask import request
from flask_restplus import Resource

from ..utils.dto import BlogDto
from ..service.blog_service import save_new_blog, get_all_blogs, get_a_blog, update_blog

api = BlogDto.api
_blog = BlogDto.blog


@api.route('/')
class BlogList(Resource):
    @api.doc('list_of_blog')
    @api.marshal_list_with(_blog, envelope='data')
    def get(self):
        return get_all_blogs()

    @api.response(201, 'Blog successfully created.')
    @api.doc('create a new blog')
    @api.expect(_blog, validate=True)
    def post(self):
        data = request.json
        return save_new_blog(data=data)

    @api.response(201, 'Blog successfully updated.')
    @api.doc('update a blog')
    @api.expect(_blog, validate=True)
    def put(self):
        data = request.json
        project = get_a_blog(data['id'])
        if not project:
            api.abort(404)
        else:
            return update_blog(data)


@api.route('/<id>')
@api.param('id', 'The Blog identifier')
@api.response(404, 'Blog not found.')
class Blog(Resource):
    @api.doc('get a blog')
    @api.marshal_with(_blog)
    def get(self, id):
        blog = get_a_blog(id)
        if not blog:
            api.abort(404)
        else:
            return blog

