from .. import db


class Skill(db.Model):
    __tablename__ = 'cv_skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ratio = db.Column(db.String(20))
    active = db.Column(db.Boolean)

    def __init__(self, name, ratio, active):
        self.name = name
        self.ratio = ratio
        self.active = active