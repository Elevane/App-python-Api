import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import blueprint
from app.main import create_app, db
from flask_cors import CORS

from app.main.model import user
from app.main.model import blog
from app.main.model import skill
from app.main.model import message
from app.main.model import project
from app.main.model import ressource

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
