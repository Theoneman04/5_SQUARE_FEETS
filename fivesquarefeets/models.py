from fivesquarefeets import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    properties = db.relationship('Property', backref='author', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Property(db.Model):
    property_id = db.Column(db.Integer, primary_key=True)
    property_title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    property_type = db.Column(db.Enum('house', 'apartment', 'office', 'retail', 'land', name='property_type_enum'), nullable=False)
    status = db.Column(db.Enum('for_sale', 'for_rent', 'pending', 'sold', name='status_enum'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text, nullable=True)  # Can store paths or URLs to images
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookings = db.relationship('Booking', backref='property', lazy=True)
    reviews = db.relationship('Review', backref='property', lazy=True)

    def __repr__(self):
        return f"Property('{self.property_title}', '{self.location}', '{self.property_type}', '{self.status}', '{self.price}')"

class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    status = db.Column(db.Enum('Confirmed', 'Pending', 'Canceled', name='booking_status_enum'), default='Confirmed', nullable=False)

    def __repr__(self):
        return f"Booking('{self.booking_id}', '{self.booking_date}', '{self.status}')"

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Assuming a rating system (e.g., 1-5)
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"Review('{self.review_id}', '{self.rating}', '{self.review_date}')"

class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.property_id'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"Wishlist('{self.wishlist_id}', '{self.date_added}')"
