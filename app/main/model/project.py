from .. import db


class Project(db.Model):
    __tablename__ = 'cv_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    description = db.Column(db.String(300))
    skills = db.Column(db.String(250))

    def __init__(self, name, image,description, skills):
        self.name = name
        self.image = image
        self.description = description
        self.skills = skills
