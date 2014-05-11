import os

from flask import Blueprint, request, url_for, redirect, render_template
from flask.ext.login import login_required
from flask_table import Table, Col, LinkCol, ButtonCol

from .models import Recipe, Ingredient, IngredientAmount, Photo, db
from .forms import RecipeForm, IngredientForm, AmountForm, PhotoForm
from datetime import datetime

from werkzeug.utils import secure_filename


class IngredientsTable(Table):
    classes = ['table']

    name = Col('Name')
    edit = LinkCol('Edit', '.ingredient_edit', url_kwargs=dict(id_='id'))
    delete = ButtonCol('Delete', '.ingredient_delete', url_kwargs=dict(id_='id'))


class AmountsTable(Table):
    name = Col('Name', attr='ingredient.name')
    amount = Col('Amount')
    edit = LinkCol('Edit', '.ingredient_edit', url_kwargs=dict(id_='id'))
    delete = ButtonCol('Delete', '.ingredient_delete', url_kwargs=dict(id_='id'))


class ManageBlueprint(Blueprint):
    def register(self, app, *args):
        self.config = {'UPLOAD_DIR': app.config['UPLOAD_DIR']}
        return Blueprint.register(self, app, *args)
    

def bp_factory():
    bp = ManageBlueprint('manage_bp', __name__, template_folder='templates')

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

    @bp.route('/amounts/addto/<int:id_>', methods=['GET', 'POST'])
    @login_required
    def amount_add(id_):
        f = AmountForm(request.form)
        if(f.validate_on_submit()):
            IngredientAmount().save_form(f, dict(recipe_id=id_))
            return redirect(url_for('index'))
        return render_template('amount_add.html', form=f)

    @bp.route('/amounts/edit/<int:id_>', methods=['GET', 'POST'])
    @login_required
    def amount_edit(id_):
        r = IngredientAmount.query.get_or_404(id_)
        f = AmountForm(request.form, obj=r)
        if(f.validate_on_submit()):
            r.save_form(f)
            return redirect(url_for('index'))
        return render_template('amount_edit.html', form=f)

    @bp.route('/amounts/delete/<int:id_>', methods=['POST'])
    @login_required
    def amount_delete(id_):
        r = IngredientAmount.query.get_or_404(id_)
        r.delete()
        return redirect(url_for('index'))

    @bp.route('/ingredients', methods=['GET', 'POST'])
    @login_required
    def ingredients():
        ings = Ingredient.query.all()
        t = IngredientsTable(ings)
        return render_template('ingredients.html', t=t)

    @bp.route('/ingredients/add', methods=['GET', 'POST'])
    @login_required
    def ingredient_add():
        f = IngredientForm(request.form)
        if(f.validate_on_submit()):
            Ingredient().save_form(f)
            return redirect(url_for('.ingredients'))
        return render_template('ingredient_add.html', form=f)

    @bp.route('/ingredients/edit/<int:id_>', methods=['GET', 'POST'])
    @login_required
    def ingredient_edit(id_):
        r = Ingredient.query.get_or_404(id_)
        f = IngredientForm(request.form, obj=r)
        if(f.validate_on_submit()):
            r.save_form(f)
            return redirect(url_for('.ingredients'))
        return render_template('ingredient_edit.html', form=f)

    @bp.route('/ingredients/delete/<int:id_>', methods=['POST'])
    @login_required
    def ingredient_delete(id_):
        r = Recipe.query.get_or_404(id_)
        r.delete()
        return redirect(url_for('ingredients'))

    def save_upload(upload):
        if upload and upload.filename:
            filename = secure_filename(upload.filename)
            filepath = os.path.join(bp.config['UPLOAD_DIR'], filename)
            upload.save(filepath)
            return filename
        else:
            return None
            

    @bp.route('/photos/add/<int:id_>', methods=['GET', 'POST'])
    @login_required
    def photo_add(id_):
        r = Recipe.query.get_or_404(id_)
        f = PhotoForm(request.form)
        saved_filename = save_upload(request.files.get('upload'))
        if f.validate_on_submit():
            extras=dict(recipe_id=r.id)
            if saved_filename:
                extras['saved_filename'] = saved_filename

            Photo().save_form(f, extras=extras)
            return redirect(url_for('index'))
        return render_template('photo_add.html', form=f)

    @bp.route('/photos/edit/<int:id_>', methods=['GET', 'POST'])
    @login_required
    def photo_edit(id_):
        p = Photo.query.get_or_404(id_)
        f = PhotoForm(request.form, obj=p)
        saved_filename = save_upload(request.files.get('upload'))
        if f.validate_on_submit():
            extras=dict()
            if saved_filename:
                extras['saved_filename'] = saved_filename
            p.save_form(f, extras=extras)
            return redirect(url_for('index'))
        return render_template('photo_edit.html', form=f)

    @bp.route('/photos/delete/<int:id_>', methods=['POST'])
    @login_required
    def photo_delete(id_):
        p = Photo.query.get_or_404(id_)
        p.delete()
        return redirect(url_for('index'))

    return bp
