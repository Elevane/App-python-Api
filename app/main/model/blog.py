from .. import db
from datetime import datetime




class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.Date, default=datetime.utcnow)
    image = db.Column(db.String(100))
    text = db.Column(db.String(500))

    def __init__(self, title, date, image, text):
        self.title = title
        self.date = date
        self.image = image
        self.text = text