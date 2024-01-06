from app import app
from flask import render_template, flash, redirect, url_for
from app.form import LoginForm

@app.route("/")
@app.route('/index')
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
    return render_template('index.html', title="Home", user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}, remember me = {form.remember_me.data}")
        return redirect('/index')
    return render_template('login.html', form=form, title='Sign In')