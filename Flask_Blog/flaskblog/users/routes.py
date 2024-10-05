from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email


# the below creates the users's blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])  # '@users' because of the 'users' 'Blueprint' above
def register():
    # to ensure that the current_user who is logged in cannot go back to the 'register.html' page:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # cont'd:
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # 'bcrypt.generate_password_hash' and 'utf-8' are used to encrypt the typed normal paswword
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')  # 'success'(a bootstrap class) here is called category in flask. It is used as a display color system for flash messages, e.g for error, it can display danger as red; or success as blue.
        return redirect(url_for('users.login'))
    return render_template("register.html", title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    # to ensure that the current_user who is logged in cannot go back to the 'login.html' page:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # cont'd:
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # 'user.password' is the password in the database. 'form.password.data' is the inputed password by the user 
            login_user(user, remember=form.remember.data)
            
            # the 2 code lines below gets executed after a user who is not logged in who tried to view a page that has 'login_required', being redirected to the login page logs in and directed to the page he wanted to view before
            next_page = request.args.get('next')  # this gets the value(page) of 'next' that usually comes as 'next=' on the google search bar when a user attempts to view a page by typing the url of the desired page on the google url bar, where user_authentication(login) is required, whereas he or she is not yet logged in
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # this returns(displays) the value(page) of 'next' if it exists, that usually comes as 'next=' on the google search bar when a user attempts to view a page by typing the url of the desired page on the google url bar, where user_authentication(login) is required, whereas he or she is not yet logged in. (It displays the page a user attempts to view but requires log in) else it goes to the 'home page' if the page is None.
        
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')  # 'danger' here is called category in flask. It is used as a display color system for flash messages, e.g for success it can display blue; or for error it displays red.
    return render_template("login.html", title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data  # 'form.username.data' is the edited(new) username(with input field) of the current_user(username.data is the new username).
        current_user.email = form.email.data  # 'form.email.data' is the edited(new) email(with input field) of the current_user(email.data is the new email).
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    
    # the below is executed to populate(fill) the input field of the account.html page with the default username and email from the database even after a reload of the account.html page. It keeps the information of the current_user in the input field as editable
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # this is created as the url of the image_file field of the User model anytime a profile pics is selected and uploaded. It upoads profile pics to this url directory. 
    return render_template("account.html", title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):  # this function is created to see all the posts created by a particular user with a username
    page = request.args.get('page', 1, type=int)  # 'page' here means the page number(not number of pages)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # 'order_by(Post.date_posted.desc())' means to display the objects in descending order on date bases, with the latest post appearing as first adn others fall under it. 'per_page' here means the number of items(content) per page.
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():  # this is for a user to request a new password, if forgotten
    # to ensure that the current_user who is logged in cannot go back to the 'login.html' page:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()  # this is the form to be filled by the user in order to get his credentials, so that another form is returned that comes with him choosing and submitting a new password
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)  # 'send_reset_email' is the function above this function. # this means if the form validates upon submission, send an email from the backend using the above function("send_reset_email") to the 'user' to reset his/her password
        flash('An email has been sent with instructions to reset your password.', 'info')  # this means if the form validates upon submission, 
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title='Request Password', form=form)
    

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):  # this is sent to the user from the backend to reset their password after they have requested for a new password. This is a function that links to the form the user fills in order to change their password
    # to ensure that the current_user who is logged in cannot go back to the 'login.html' page:
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 

    user = User.verify_reset_token(token)  # 'verify_reset_token(token)' is the function created under the User model in model.py file as function to verify the token sent to the user
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()  # this form is returned from the backend so that the user can choose and submit a new password after he has made a request for a new password
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # 'bcrypt.generate_password_hash' and 'utf-8' are used to encrypt the inputed password
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')  # 'success'(a bootstrap class) here is called category in flask. It is used as a display color system for flash messages, e.g for error, it can display danger as red; or success as blue.
        return redirect(url_for('users.login'))
    
    return render_template("reset_token.html", title='Reset Password', form=form)
    


