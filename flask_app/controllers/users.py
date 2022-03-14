from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.valid(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.registration(data)
    session['user_id'] = id
    return redirect('/dashboard')    


@app.route('/login', methods=['POST'])
def login_user():
    user = User.get_email(request.form)
    
    if not User.valid(request.form):
        flash('Invalid Email. Please try again or register an account.','login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password. Please try again','login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')   


@app.route ('/dashboard')
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    return render_template('dashboard.html', user = User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')