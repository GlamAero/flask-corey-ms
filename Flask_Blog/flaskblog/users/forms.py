from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    # to validate the inputed username(to check if there is an of an existence of the inputed username in the database)
    def validate_username(self, username):  # 'username' because we want to check if username exists already or not. If it exists, it inputs an error.
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one.')
            
    # to validate the inputed email(to check if there is an of an existence of the inputed email in the database)
    def validate_email(self, email):  # 'email' because we want to check if email exists already or not. If it exists, it outputs an error.
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one.')
    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])  # this is used to update the profile picture
    submit = SubmitField('Update')
    
    # to validate the inputed username(to check if there is an of an existence of the inputed username in the database)
    def validate_username(self, username):  # 'username' because we want to check if username exists already or not. If it exists, it inputs an error.
        if username.data != current_user.username:  # 'username.data' is the edited(new) username(with input field) of the current_user(username.data is the new username). 'current_user.username' is the previous username that is registered by the current_user on the database.
            user = User.query.filter_by(username=username.data).first()  # this means if there exists a username(username) of another user that is the same name as the newly created username(username.data) of the current_user
            if user:
                raise ValidationError('That username is taken, please choose a different one.')
                
    # to validate the inputed email(to check if there is an of an existence of the inputed email in the database)
    def validate_email(self, email):  # 'email' because we want to check if email exists already or not. If it exists, it inputs an error.
        if email.data != current_user.email:  # 'email.data' is the edited(new) email(with input field) of the current_user(email.data is the new email). 'current_user.email' is the previous email that is registered by the current_user on the database.
            user = User.query.filter_by(email=email.data).first()  # this means if there an email(email) of another user that is the same name as the newly created email(email.data) of the current_user
            if user:
                raise ValidationError('That email is taken, please choose a different one.')


# the class below creates a form for resetting password through email. It is by a user for 'requesting' for a password reset. This form is sent to the backend by the user 
class RequestResetForm(FlaskForm):  # this class is used with the function- 'get_reset_token' and 'verify_reset_token' under the User model class in the 'models.py' file to reset a user password upon request by the user
    email = StringField('Email', validators=[DataRequired(), Email()])    
    submit = SubmitField('Request Password Reset')
    
    # to validate the inputed email(to check if there is an of an existence of the inputed email in the database)
    def validate_email(self, email):  # 'email' because we want to check if email exists already or not. If it does not exist, it outputs an error.
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        

class ResetPasswordForm(FlaskForm):  # this form is sent from the backend to the user to fill so as to reset his password, after the user has sent the 'RequestResetForm' to the backend. This is a response to that request.
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')




