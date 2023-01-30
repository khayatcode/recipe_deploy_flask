from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('log_in.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_regist(request.form):
        # we redirect to the template with the form.
        return redirect('/')  
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(user_data)
    print(user_id)
    session['user_id'] = user_id # this equals the id
    
    return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid Email/Password!","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password!", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/recipes')


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')
