from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 


#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# db
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

#init Marchmallow

ma = Marchmallow(app)

#Ressource Class/model
class Ressource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unity = db.Column(db.String(20))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    #user = db.relationship("User")

    def __init__(self, name, quantity, unity):#, user):
        self.name = name
        self.quantity = quantity
        self.unity = unity
        #self.user = user

class RessourceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'quantity', 'unity')#,'user')


#init Schema

ressource_schema = RessourceSchema(strict=True)
ressources_schema = RessourceSchema(many = True, strict=True)
#run server

if __name__ == '__main__':
    app.run(debug=true)