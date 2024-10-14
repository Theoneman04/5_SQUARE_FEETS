import os
import secrets
from PIL import Image
from flask import Blueprint, current_app,render_template, url_for, flash, redirect, request
from fivesquarefeets import db
from fivesquarefeets.forms import RegistrationForm, LoginForm, UpdateAccountForm
from fivesquarefeets.models import User, Property
from flask_login import login_user, current_user, logout_user, login_required

# Create a Blueprint for your routes
bp = Blueprint('main', __name__)

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/about")
def about():
    image_f = url_for('static', filename='home_long.jpeg')
    return render_template('about.html', title='About',image_f=image_f)

@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        with current_app.app_context():  # Use current_app instead of app
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.login'))  # Update to reference blueprint
    return render_template('register.html', title='Register', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # Update to reference blueprint
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # Update to reference blueprint
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))  # Update to reference blueprint

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(bp.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))  # Update to reference blueprint
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
