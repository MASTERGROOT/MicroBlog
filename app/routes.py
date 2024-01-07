from app import app, db
from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from app.form import LoginForm, Registration
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User

@app.route("/")
@app.route('/index')
@login_required
def index():
    user = {'username': 'Goody'}
    posts = [
        {
            'author': {'username': 'Fernando'},
            'body': "I love car!"
        },
        {
            'author': {'username': 'Nate'},
            'body': "Busch Garden For every!!!"
        }
    ]
    return render_template('index.html', title="Home Page", posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # user is already logged in, redirect to the index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    regis_form = Registration()
    if regis_form.validate_on_submit():
        user = User(username=regis_form.username.data, email=regis_form.email.data)
        user.set_password(regis_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', regis_form=regis_form)