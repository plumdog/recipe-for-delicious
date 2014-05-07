from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin):
    id = 1


class FormSaveable(object):
    def save_form(self, form, extras={}, commit=True):
        for f in form:
            setattr(self, f.name, f.data)
        for k, v in extras.items():
            setattr(self, k, v)
        db.session.add(self)
        if commit:
            db.session.commit()

        return self


class Deletable(object):
    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self


class Base(db.Model, FormSaveable, Deletable):
    __abstract__ = True


class Recipe(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    posted_on = db.Column(db.DateTime)
