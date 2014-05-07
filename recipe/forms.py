from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField
from wtforms.validators import Required


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])


class RecipeForm(Form):
    title = StringField('Title', [Required()])
    posted_on = DateTimeField(
        'Date Posted', [Required()],
        format='%d/%m/%Y %H:%M', description='dd/mm/yyyy hh:mm')
    content = TextAreaField('Content', [Required()])
