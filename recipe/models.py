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


class Dropdown(object):
    @classmethod
    def dropdown(cls, key_col='id', value_col='name'):
        out = []
        for r in cls.query.order_by(value_col).all():
            out.append(
                (int(getattr(r, key_col)),
                 str(getattr(r, value_col))))
        print(out)
        return out


class Deletable(object):
    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
        return self


class Base(db.Model, FormSaveable, Deletable, Dropdown):
    __abstract__ = True


class Recipe(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    posted_on = db.Column(db.DateTime)


class Ingredient(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class IngredientAmount(Base):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    amount = db.Column(db.String(100))

    recipe = db.relationship('Recipe', backref=db.backref('ingredient_amounts', lazy='dynamic'))
    ingredient = db.relationship('Ingredient', backref=db.backref('ingredient_amounts', lazy='dynamic'))
