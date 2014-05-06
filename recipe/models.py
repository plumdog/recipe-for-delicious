from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin):
    id = 1
