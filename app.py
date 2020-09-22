from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS, cross_origin
import os



# Init app
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bastienaquba:5cEhQfzLS37vDuE@bastienaquba.mysql.db:3306/bastienaquba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

#Ressource Class/model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    ressource = db.relationship("Ressource")


    def __init__(self, login, password):
        self.login = login
        self.password = password


class Ressource(db.Model):
    __tablename__ = 'course_ressource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unity = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, name, quantity, unity, user):
        self.name = name
        self.quantity = quantity
        self.unity = unity
        self.user = user


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'login', 'password')


class RessourceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'quantity', 'unity','user')

# POST ressource
@app.route('/ressource', methods=['POST'])
def add_ressource():
    name = request.json['name']
    quantity = request.json['quantity']
    unity = request.json['unity']
    user = request.json['user']

    res = Ressource(name, quantity, unity, user)
    db.session.add(res)
    db.session.commit()

    return ressource_schema.jsonify(res)


# Get All Ressources
@app.route('/ressource', methods=['GET'])
def get_ressources():
  all_ressources = Ressource.query.all()
  result = ressources_schema.dump(all_ressources)
  return jsonify(result)

@app.route('/ressource/<id>', methods=['GET'])
def get_ressource(id):
    res = Ressource.query.get(id)
    return ressource_schema.jsonify(res)


#init Schema

ressource_schema = RessourceSchema()
ressources_schema = RessourceSchema(many = True)
#run server

if __name__ == '__main__':
    app.run(debug=True)