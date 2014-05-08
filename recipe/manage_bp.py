from flask import Blueprint, request, url_for, redirect, render_template
from flask.ext.login import login_required

from .models import Recipe, db
from .forms import RecipeForm
from datetime import datetime

def bp_factory():
    bp = Blueprint('manage_bp', __name__, template_folder='templates')

    @bp.route('/add', methods=['GET', 'POST'])
    @login_required
    def add():
        f = RecipeForm(request.form)
        if(f.validate_on_submit()):
            Recipe().save_form(f)
            return redirect(url_for('index'))
        f.posted_on.data = datetime.now()
        return render_template('add.html', form=f)

    @bp.route('/edit/<int:id_>', methods=['GET', 'POST'])
    @login_required
    def edit(id_):
        r = Recipe.query.get_or_404(id_)
        f = RecipeForm(request.form, obj=r)
        if(f.validate_on_submit()):
            r.save_form(f)
            return redirect(url_for('index'))
        return render_template('edit.html', form=f)


    @bp.route('/delete/<int:id_>', methods=['POST'])
    @login_required
    def delete(id_):
        r = Recipe.query.get_or_404(id_)
        r.delete()
        return redirect(url_for('index'))

    return bp
