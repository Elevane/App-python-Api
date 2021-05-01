from .. import db


def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except:
        db.session.rollback()
        raise


def delete(data):

    try:
        db.session.delete(data)
        db.session.commit()
    except:
        db.session.rollback()
        raise
