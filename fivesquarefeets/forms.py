from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import IntegerField,StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from fivesquarefeets.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign_up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# New form to add property
class PropertyForm(FlaskForm):
    property_title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=5, max=100)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10)])
    property_type = SelectField('Property Type', choices=[('house', 'House'), ('apartment', 'Apartment'),
                                                          ('office', 'Office'), ('retail', 'Retail'), ('land', 'Land')],
                                validators=[DataRequired()])
    status = SelectField('Status', choices=[('for_sale', 'For Sale'), ('for_rent', 'For Rent'),
                                            ('pending', 'Pending'), ('sold', 'Sold')], validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])
    images = FileField('Property Images (optional)', validators=[FileAllowed(['jpg', 'png', 'webp'])])
    submit = SubmitField('Update Property')  # Change the label to 'Update Property'

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Review')