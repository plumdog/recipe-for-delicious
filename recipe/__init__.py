from flask import Flask, render_template, request, redirect, flash, url_for, abort
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required, login_url
from .models import db, User
from .forms import LoginForm

from flask_debugtoolbar import DebugToolbarExtension

import config_combined

def string_isinstance(obj, cls_name):
    return cls_name in [type_.__name__ for type_ in obj.__class__.__bases__] + [type(obj).__name__]

def app_factory(**kwargs):
    app = Flask(__name__)
    app.config.from_object(config_combined)
    db.init_app(app)

    DebugToolbarExtension(app)

    app.add_template_global(string_isinstance, name='string_isinstance')

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        form = LoginForm(request.form)
        if form.validate_on_submit():
            if (form.username.data == app.config['ADMIN_USERNAME'] and
                form.password.data == app.config['ADMIN_PASSWORD']):
                user = User()
                login_user(user)
                return redirect(url_for('index'))
            else:
                form.username.errors.append('Invalid Username...')
                form.password.errors.append('...or Password')
        return render_template('login.html', form=form)

    @app.route('/logout/')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/content/')
    @login_required
    def content():
        return render_template('content.html')

    @app.errorhandler(404)
    def err404(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def err500(e):
        return render_template('500.html'), 500

    return app
