
from .. import db


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, email, message, title, name):
        self.email = email
        self.message = message
        self.title = title
        self.name = name
