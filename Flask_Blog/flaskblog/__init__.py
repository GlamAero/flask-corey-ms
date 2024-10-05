from flask import Flask
from flask_sqlalchemy import SQLAlchemy  
from flask_bcrypt import Bcrypt  
from flask_login import LoginManager
from flask_mail import Mail  
from flaskblog.config import Config


# creating objects of the different components:
db = SQLAlchemy()  
bcrypt = Bcrypt()  
login_manager = LoginManager()  # this is used to manage the login of users

login_manager.login_view = 'users.login'  # this states the function name('login') of our route/url that is -login, wherein to redirect a user who attempts to view a page(by typing the url of the desired page on the google url bar) where user_authentication(login) is required whereas he or she is not yet logged in
login_manager.login_message_category = 'info'  # this is used to add color('info') to the flash message produced when a user who attempts to view a page(by typing the url of the desired page on the google url bar) where user_authentication(login) is required whereas he or she is not yet logged in

# creating the object of the mail for sending email of password reset to the user
mail = Mail()


# to create different instances of the app with different configurations, a function(create_app) is created to return the app instance and the app instance is created in the __init__.py file
def create_app(config_class=Config):  # 'Config' is the class in the 'config.py' file
    
    # this creates the flask app:
    app = Flask(__name__)
    
    # this connects the config.py file to this init.py file:
    app.config.from_object(Config)  
    
    # initializing components:
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # to create the database:
    app.app_context().push()  # this pushes the app context to the app
    db.create_all()  # this creates the database

    # Blueprint registration:(the blue prints are in the routes of the different elements folders like users folder route.py, main folder route.py, post folder route.py)
    from flaskblog.users.routes import users  
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app
    
