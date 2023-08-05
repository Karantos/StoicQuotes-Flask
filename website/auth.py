from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Username does not exist.', category='error')


    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirm-password')

        user = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user:
            flash('Username taken', category='error')
        elif user_email:
            flash('Email already used', category='error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        elif password != confirmation:
            flash('Passwords do not match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', category='success')
            return redirect(url_for('views.index'))

        return render_template('register.html')
    else:

        return render_template('register.html')

@auth.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')

        user_id = User.get_id(current_user)

        if len(email) < 4:
            flash('Email must be at least 4 characters long.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        else:
            User.query.filter_by(id=user_id).update(dict(username=username, email=email))
            db.session.commit()
            flash('Profile updated!', category='success')
            return redirect(url_for('views.index'))

        return render_template('edit_profile.html')
    else:

        return render_template('edit_profile.html')

@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('password')
        new_password = request.form.get('new-password')
        confirmation = request.form.get('confirm-password')

        user_id = User.get_id(current_user)
        user = User.query.filter_by(id=user_id).first()

        if not check_password_hash(user.password, old_password):
            flash('Passwords is incorrect!', category='error')
        elif new_password != confirmation:
            flash('Passwords do not match.', category='error')
        elif len(new_password) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            User.query.filter_by(id=user_id).update(dict(password=generate_password_hash(new_password, method='sha256')))
            db.session.commit()
            flash('Password changed!', category='success')
            logout_user()
            return redirect(url_for('auth.login'))

        return render_template('change_password.html')
    else:

        return render_template('change_password.html')