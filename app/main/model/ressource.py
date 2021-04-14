from .. import db

class Ressource(db.Model):
    __tablename__ = 'ressource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unity = db.Column(db.String(20))

    def __init__(self, name, quantity, unity):
        self.name = name
        self.quantity = quantity
        self.unity = unity

