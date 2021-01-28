from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import os
from datetime import datetime, date


# Init app
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)



class Count(db.Model):
    __tablename__ = 'compteur_count'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)

    def __init__(self, count):
        self.count = count


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Ressource(db.Model):
    __tablename__ = 'course_ressource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    unity = db.Column(db.String(20))

    def __init__(self, name, quantity, unity):
        self.name = name
        self.quantity = quantity
        self.unity = unity


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


class Blog(db.Model):
    __tablename__ = 'cv_blog'
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


class Project(db.Model):
    __tablename__ = 'cv_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(100))
    skills = db.Column(db.String(250))

    def __init__(self, name, image, skills):
        self.name = name
        self.image = image
        self.skills = skills


class BlogSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'date', 'image', 'text')


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'image', 'skills')


class SkillsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'ratio', 'active')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password')


class RessourceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'quantity', 'unity', 'user')


@app.route('/', methods=['GET'])
def status():
    return True


@app.route('/getuser', methods=['POST'])
def get_user():
    print(request)
    res = User.query.filter_by(
        email=request.json['username'], password=request.json['password']).first()
    print(res)
    return user_schema.jsonify(res)


@app.route('/user', methods=['POST'])
def add_user():
    email = request.json['username']
    password = request.json['password']

    res = User(email, password)
    db.session.add(res)
    db.session.commit()

    return user_schema.jsonify(res)


########## BLOG #################
######################################
@app.route('/blog', methods=['POST'])
def add_blog():
    title = request.json['title']
    date = processDate(request.json['date']['date'])
    image = request.json['image']
    text = request.json['text']

    res = Blog(title, date, image, text)
    db.session.add(res)
    db.session.commit()

    return blog_schema.jsonify(res)

## Delete Blog


@app.route('/blog/<id>', methods=['DELETE'])
def delete_blog(id):
  res = Blog.query.get(id)
  db.session.delete(res)
  db.session.commit()

  return blog_schema.jsonify(res)

# Get All Blogs


@app.route('/blog', methods=['GET'])
def get_blogs():
  all_blogs = Blog.query.all()
  result = blogs_schema.dump(all_blogs)
  return jsonify(result)

  # Get one Blog


@app.route('/blog/<id>', methods=['GET'])
def get_blog(id):
  blog = Blog.query.get(id)
  print(blog)
  res = blog_schema.dump(blog)
  return jsonify(res)

# Get one blog


@app.route('/blog', methods=['PATCH'])
def update_blog():
  blog = Blog.query.get(request.json['id'])
  blog.title = request.json['title']
  blog.date = processDate(request.json['date']['date'])
  blog.image = request.json['image']
  blog.text = request.json['text']
  db.session.commit()
  print(processDate(request.json['date']['date']))

  return jsonify(res)
######################################


@app.route('/project', methods=['POST'])
def add_project():
    name = request.json['name']
    image = request.json['image']
    skills = request.json['skills']
    res = Project(name, image, skills)
    db.session.add(res)
    db.session.commit()

    return Project_schema.jsonify(res)

## Delete project


@app.route('/project/<id>', methods=['DELETE'])
def delete_project(id):
  res = Project.query.get(id)
  db.session.delete(res)
  db.session.commit()

  return Project_schema.jsonify(res)

# Get All Projects


@app.route('/project', methods=['GET'])
def get_projects():
  all_Projects = Project.query.all()
  result = Projects_schema.dump(all_Projects)
  return jsonify(result)

# Get one project


@app.route('/project/<id>', methods=['GET'])
def get_project(id):
  project = Project.query.get(id)
  print(project)
  res = Project_schema.dump(project)
  return jsonify(res)


# Get one project
@app.route('/project', methods=['PATCH'])
def update_project():
  project = Project.query.get(request.json['id'])
  project.name = request.json['name']
  project.image = request.json['image']
  project.skills = request.json['skills']
  db.session.commit()
  print(request.json['name'])

  res = skill_schema.dump(project)
  return jsonify(res)


######################################

## create one skill
@app.route('/skill', methods=['POST'])
def add_skills():
    name = request.json['name']
    ratio = request.json['ratio']
    active = request.json['active']
    res = Skill(name, ratio, active)
    db.session.add(res)
    db.session.commit()

    return ressource_schema.jsonify(res)

## Delete one skill


@app.route('/skill/<id>', methods=['DELETE'])
def delete_skill(id):
  res = Skill.query.get(id)
  db.session.delete(res)
  db.session.commit()

  return ressource_schema.jsonify(res)

# Get All skills


@app.route('/skill', methods=['GET'])
def get_skills():
  all_skills = Skill.query.all()
  result = Skills_schema.dump(all_skills)
  return jsonify(result)

# Get one skill


@app.route('/skill/<id>', methods=['GET'])
def get_skill(id):
  skill = Skill.query.get(id)
  res = skill_schema.dump(skill)
  return jsonify(res)

# Get one skill


@app.route('/skill', methods=['PATCH'])
def update_skill():
  skill = Skill.query.get(request.json['id'])
  skill.name = request.json['name']
  skill.ratio = request.json['ratio']
  skill.active = request.json['active']
  db.session.commit()

  res = skill_schema.dump(skill)
  return jsonify(res)


######################################
@app.route('/ressource', methods=['POST'])
def add_ressource():
    name = request.json['name']
    quantity = request.json['quantity']
    unity = request.json['unity']

    res = Ressource(name, quantity, unity)
    db.session.add(res)
    db.session.commit()

    return ressource_schema.jsonify(res)

## Delete Ressource


@app.route('/ressource/<id>', methods=['DELETE'])
def delete_ressource(id):
  res = Ressource.query.get(id)
  db.session.delete(res)
  db.session.commit()

  return ressource_schema.jsonify(res)

# Get All Ressources


@app.route('/ressource', methods=['GET'])
def get_ressources():
  all_ressources = Ressource.query.all()
  result = ressources_schema.dump(all_ressources)
  return jsonify(result)


def processDate(date):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return datetime(year, month, day)

#init Schema


user_schema = UserSchema()


blog_schema = BlogSchema()
blogs_schema = BlogSchema(many=True)

Project_schema = ProjectSchema()
Projects_schema = ProjectSchema(many=True)

ressource_schema = RessourceSchema()
ressources_schema = RessourceSchema(many=True)

skill_schema = SkillsSchema()
Skills_schema = SkillsSchema(many=True)
#run server


if __name__ == '__main__':
    app.run(debug=True)
