from flask import Blueprint, request, url_for, redirect, render_template
from flask.ext.login import login_required
from flask_table import Table, Col, LinkCol, ButtonCol

from .models import Recipe, Ingredient, IngredientAmount, db
from .forms import RecipeForm, IngredientForm, AmountForm
from datetime import datetime


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
        

    return bp
