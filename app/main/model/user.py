from .. import db, flask_bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


@property
def password(self):
    raise AttributeError('password: write-only field')


@password.setter
def password(self, password):
    self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(self, password):
    return flask_bcrypt.check_password_hash(self.password_hash, password)


def create_seeds():
    db.session.add(User(email='Admin', password='Moltencore1993!'))
    db.session.commit()

