from flask import render_template, url_for, flash, redirect, request
from fivesquarefeets import app, db
from fivesquarefeets.forms import RegistrationForm, LoginForm
from fivesquarefeets.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required



posts=[
        {
            'author': 'Anjana',
            'title': 'Blog Post',
            'content': 'first post content',
            'date_posted': 'Apwril 21,2018'
        },
        {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'second post content',
        'date_posted': 'May 21,2018'
        }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user= User(username=form.username.data, email=form.email.data,password=form.password.data)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form= form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password==form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',title='Login', form= form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')
