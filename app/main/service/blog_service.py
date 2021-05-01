import uuid
from datetime import datetime

from app.main import db
from app.main.model.blog import Blog
from app.main.utils.SessionManager import save_changes, delete

def save_new_blog(data):
    blog = Blog.query.filter_by(title=data['title']).first()
    if not blog:
        new_blog = Blog(
            title=data['title'],
            image=data['image'],
            text=data['text'],
            date=data['date'],
        )
        save_changes(new_blog)
        response_object = {
            'status': 'success',
            'message': 'blog Successfully created.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Blog already exists',
        }
        return response_object, 409


def get_all_blogs():
    return Blog.query.all()


def get_a_blog(blog_id):
    return Blog.query.filter_by(id=blog_id).first()


def delete_blog(blog_id):
    res = Blog.query.get(blog_id)
    if res:
        delete(res)


def update_blog(data):
    blog = Blog.query.get(data['id'])
    if blog:
        blog.title = data['title']
        blog.image = data['image']
        blog.text = data['text']
        blog.date = process_date(data['date'])
        save_changes(blog)
        response_object = {
            'status': 'success',
            'message': 'Successfully updated.'
        }
        return response_object, 201

    else:
        response_object = {
            'status' : 'fail',
            'message' : 'Object doesn\'t exist'
        }

        return response_object, 409


def process_date(date):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    return datetime(year, month, day)