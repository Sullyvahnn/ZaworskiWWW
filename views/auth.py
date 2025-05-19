from flask import render_template, Blueprint, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, login_required, logout_user

from models import User, db
from views.main import serve_base

auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup_form():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered')
            return redirect(url_for('auth.signup_form'))

        # Hash the password securely
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        new_user = User(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.index'))

    return render_template('signup.html')

@auth.route('/login')
def login_form():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Cant log in, please check your profile data')
            return redirect(url_for('auth.login_form'))

        login_user(user)
        return redirect(url_for('main.index', user_id=user.id))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.serve_base'))





