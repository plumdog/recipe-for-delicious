from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import Required


from .models import Ingredient

from config_combined import ALLOWED_EXTENSIONS


def int_or_none(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return None

class DbSelectField(SelectField):
    def __init__(self, *args, **kwargs):
        kwargs['coerce'] = int_or_none
        super().__init__(*args, **kwargs)


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])


class RecipeForm(Form):
    title = StringField('Title', [Required()])
    posted_on = DateTimeField(
        'Date Posted', [Required()],
        format='%d/%m/%Y %H:%M', description='dd/mm/yyyy hh:mm')
    content = TextAreaField('Content', [Required()])


class IngredientForm(Form):
    name = StringField('Name', [Required()])


class AmountForm(Form):
    amount = StringField('Amount')
    ingredient_id = DbSelectField('Ingredient')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.ingredient_id.choices = Ingredient.dropdown()

class PhotoForm(Form):
    tag = StringField('Tag', [Required()])
    upload = FileField('Photo', validators=[FileAllowed(list(ALLOWED_EXTENSIONS), 'Invalid file type. Must be ' + ', '.join(list(ALLOWED_EXTENSIONS)))])
