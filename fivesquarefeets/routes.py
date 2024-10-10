import os
import secrets
from PIL import Image
from flask import Blueprint, current_app, render_template, url_for, flash, redirect, request
from fivesquarefeets import db
from fivesquarefeets.forms import RegistrationForm, LoginForm, UpdateAccountForm, PropertyForm
from fivesquarefeets.models import User, Property,Wishlist,Booking,Review
from flask_login import login_user, current_user, logout_user, login_required

# Create a Blueprint for your routes
bp = Blueprint('main', __name__)

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/about")
def about():
    return render_template('about.html', title='About')

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

@bp.route("/myproperty", methods=['GET'])
@login_required
def myproperty():
    # Fetch all properties added by the current user
    properties = Property.query.filter_by(user_id=current_user.id).all()
    return render_template('myproperty.html', title='My Property', properties=properties)

# Function to save property images
def save_property_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(bp.root_path, 'static/property_pics', image_fn)

    output_size = (800, 800)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn

@bp.route("/property/new", methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        if form.images.data:
            image_file = save_property_image(form.images.data)
        else:
            image_file = None

        property = Property(
            property_title=form.property_title.data,
            location=form.location.data,
            address=form.address.data,
            property_type=form.property_type.data,
            status=form.status.data,
            price=form.price.data,
            description=form.description.data,
            images=image_file,
            author=current_user
        )

        db.session.add(property)
        db.session.commit()
        flash('Your property has been added!', 'success')
        return redirect(url_for('main.myproperty'))  # Redirect to "My Property" page

    return render_template('add_property.html', title='New Property', form=form)

@bp.route("/property1/<int:property_id>")
@login_required
def view_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.author != current_user:
        flash('You do not have permission to view this property.', 'danger')
        return redirect(url_for('main.myproperty'))
    return render_template('view_property.html', title=property.property_title, property=property)

@bp.route("/property/<int:property_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    property = Property.query.get_or_404(property_id)
    
    if property.author != current_user:
        flash('You do not have permission to edit this property.', 'danger')
        return redirect(url_for('main.myproperty'))

    form = PropertyForm()

    if form.validate_on_submit():
        property.property_title = form.property_title.data
        property.location = form.location.data
        property.address = form.address.data
        property.property_type = form.property_type.data
        property.status = form.status.data
        property.price = form.price.data
        property.description = form.description.data
        
        if form.images.data:
            # If a new image is uploaded, save it
            image_file = save_property_image(form.images.data)
            property.images = image_file  # Update the image field
            
        db.session.commit()
        flash('Your property has been updated!', 'success')
        return redirect(url_for('main.myproperty'))  # Redirect to myproperty page

    elif request.method == 'GET':
        form.property_title.data = property.property_title
        form.location.data = property.location
        form.address.data = property.address
        form.property_type.data = property.property_type
        form.status.data = property.status
        form.price.data = property.price
        form.description.data = property.description

    return render_template('edit_property.html', title='Edit Property', form=form, property=property)

@bp.route("/property/<int:property_id>/delete", methods=['POST'])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    
    if property.author != current_user:
        flash('You do not have permission to delete this property.', 'danger')
        return redirect(url_for('main.myproperty'))

    # Optionally, delete the image file(s) from the server
    if property.images:
        image_files = property.images.split(',')
        for image_file in image_files:
            image_path = os.path.join(bp.root_path, 'static/property_pics', image_file.strip())
            if os.path.exists(image_path):
                os.remove(image_path)
    
    db.session.delete(property)
    db.session.commit()
    flash('Your property has been deleted!', 'success')
    return redirect(url_for('main.myproperty'))
@bp.route("/property")
def all_properties():
    properties = Property.query.all()  # Fetch all properties
    return render_template('all_properties.html', title='All Properties', properties=properties)

@bp.route("/property/<int:property_id>")
def detailed_view(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('detailed_view.html', property=property)

@bp.route("/property/<int:property_id>/add_to_wishlist", methods=['POST'])
@login_required
def add_to_wishlist(property_id):
    property = Property.query.get_or_404(property_id)

    # Check if the property is already in the wishlist
    existing_wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, property_id=property_id).first()
    if existing_wishlist_item:
        flash('This property is already in your wishlist!', 'info')
    else:
        # Create a new wishlist item
        wishlist_item = Wishlist(user_id=current_user.id, property_id=property_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('The property has been added to your wishlist!', 'success')

    return redirect(url_for('main.detailed_view', property_id=property_id))

@bp.route("/wishlist")
@login_required
def wishlist():
    # Fetch the current user's wishlist with property details
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    wishlist_properties = [Property.query.get(item.property_id) for item in wishlist_items]
    return render_template('wishlist.html', wishlist_properties=wishlist_properties)


@bp.route("/delete_from_wishlist/<int:property_id>", methods=["POST"])
@login_required
def delete_from_wishlist(property_id):
    # Find the wishlist entry to delete
    wishlist_entry = Wishlist.query.filter_by(user_id=current_user.id, property_id=property_id).first()
    if wishlist_entry:
        db.session.delete(wishlist_entry)
        db.session.commit()
        flash("Property removed from wishlist.", "success")
    else:
        flash("Property not found in wishlist.", "error")
    return redirect(url_for('main.wishlist'))

