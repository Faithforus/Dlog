from app.ext import db


class Base(db.Model):
    __abstract__ = True

    def set_attrs(self, attrs):
        for key, value in attrs.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def add(self, model):
        db.session.add(model)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
        return None
    except Exception as e:
        db.session.rollback()
        return str(e)


import app.model.recycle
import app.model.blog
import app.model.blogger
import app.model.comment
import app.model.setting
import app.model.guest
