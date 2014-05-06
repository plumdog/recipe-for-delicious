from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import Required


class LoginForm(Form):
    username = StringField('Username', [Required()])
    password = PasswordField('Password', [Required()])
