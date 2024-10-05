from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):  # this is used for login where if the user inputs a wrong email, it gives our own created flash message rather than the flask default message. It overides the existing flask error message
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # 'Post' means that posts has a relationship with the 'Post' model. "backref='author'" means 'author should ordinarily be in the 'Post' model as a table, but it has a relationship with the Post model(The relationship is a 'one to many' relationship; that is 'one author/user making many posts' but 'one post belongs to only one author/user'). 'lazy=True' means SQLAlchemy will load the database in one go. 'author' alone gives 'Úser.query.all()'; meaning it gives the entire User object elements -('username', 'email' and 'image_file')
    
    def get_reset_token(self):  # this function along with the one below were created to reset a user's password if the user forgot their password. This function works with a form called 'ResetPasswordForm' and another form called'RequestResetForm' both in 'form.py'.
        s = Serializer(current_app.secret_key)
        return s.dumps({'user_id': self.id})
    
    @staticmethod  # 'static method' means the function below should not expect a 'self' argument but only one argument('token')
    def verify_reset_token(token):  # this function along with the one above were created to reset a user's password if the user forgot their password. This function works with a form called 'ResetPasswordForm'and another form called'RequestResetForm' both in 'form.py'.
        s = Serializer(current_app.secret_key)
        try:
            user_id = s.loads(token, max_age=1800)['user_id']  # max_age is the time(in seconds) within which a user can change their password upon request, else the request expires and then the user may have to make a request for password change again
        except:
            return None  # this means if 'user_id = s.loads(token)['user_id']' gives error, return no value
        return User.query.get(user_id)  # this means if 'user_id = s.loads(token)['user_id']' works well and gives no error, return this user- 'User.query.get(user_id)'
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
