from flask_restplus import Api
from flask import Blueprint
from werkzeug.utils import cached_property
from .main.controller.project_controller import api as project_ns
from .main.controller.blog_controller import api as blog_ns
from .main.controller.message_controller import api as message_ns
from .main.controller.ressource_controller import api as ressource_ns
from .main.controller.skill_controller import api as skill_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API',
          version='1.0',
          description='personnal api for many services'
          )

api.add_namespace(project_ns, path='/project')
api.add_namespace(blog_ns, path='/blog')
api.add_namespace(message_ns, path='/message')
api.add_namespace(ressource_ns, path='/ressource')
api.add_namespace(skill_ns, path='/skill')
