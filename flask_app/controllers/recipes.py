from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/recipes')
def logged_in():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('home_page.html', user = User.get_one(data), all_the_recipes = Recipe.get_all_recipes_with_creator())

@app.route('/create_recipe', methods = ['POST'])
def save():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe_data(request.form):
        # we redirect to the template with the form.
        return redirect('/recipe/new')
    print(request.form)
    data = {
        "user_id": session['user_id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date_made": request.form['date_made'],
        "under_30": request.form['under_30']
    }
    Recipe.save(data)
    return redirect('/recipes')

@app.route('/recipe/new')
def new_recipe_page():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_recipe.html")

@app.route('/edit/<int:id>')
def r_update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    return render_template('edit_recipe.html', recipe = Recipe.get_one(data))

@app.route('/view/<int:id>')
def r_view_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    return render_template('view_recipe.html', recipe = Recipe.get_one(data))

@app.route('/edit_recipe', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe_data(request.form):
        return redirect(f"/edit/{request.form['id']}")
    Recipe.update(request.form)
    return redirect('/recipes')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': id
    }
    Recipe.delete(data)
    print(f"id is {id}")
    return redirect('/recipes')