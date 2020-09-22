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
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

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
    user = db.relationship("User", back_populates="ressources")


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




#init Schema

ressource_schema = RessourceSchema(strict=True)
ressources_schema = RessourceSchema(many = True, strict=True)
#run server

if __name__ == '__main__':
    app.run(debug=true)