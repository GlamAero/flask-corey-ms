import os


class Config:
    # to set up the database use:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # this(it's value is saved in the user environment variable of this system(laptop)) is used to protect the form/app, just like CSRF_TOKEN in django
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # this(it's value is saved in the user environment variable of this system(laptop)) is for the sqlite database

    # the below are for setting up the email system so as to send mails from this app to the server and from the server to this app
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # 'EMAIL_USER's value is saved in environment variable(user variable section) of this laptop
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # 'EMAIL_PASS's value is saved in environment variable(user variable section) of this laptop

