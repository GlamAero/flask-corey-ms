import os
import secrets
from PIL import Image  # PIL was got from the installed Pillow package
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message


def save_picture(form_picture):  # form_picture is the picture picked for upload by the current_user
    random_hex = secrets.token_hex(8)  # this converts in hex(8) format for ease of reading/decoding on the system
    _, f_ext = os.path.splitext(form_picture.filename)  # here the picture('form_picture') is picked and splitted for ease of conversion to hex format so that the code will be able to read and output it as appropriate
    picture_fn = random_hex + f_ext  # this converts(in hex) the picture that was picked by the current user. It is converted for easy reading by the code system
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # this shows how movement of the picture('picture_fn') from 'current_app.root_path' to the final destination('static/profile_pics'). 'app.root_path' is the source location where the image was picked from. 'static/profile_pics' is the location where the picture picked will be saved upon being uploaded as profile pics.
    
    output_size = (125, 125)  # this means to resize the image to 125px on the length and width
    i = Image.open(form_picture)  # i now becomes the new image. the old image('form_picture') is open for use 
    i.thumbnail(output_size)  # here the image('form_picture') is thumbnailed to the output size, such that it gets resized to the output size
    i.save(picture_path)  # here the image('form_picture') is then saved to the 'picture_path' directory
    
    return picture_fn  # this then return the converted(in hex format) formatted of the 'form_picture' when this function is called
    
    
def send_reset_email(user):  # this function is created to send an email to the user to change his password when forgotten
    token = user.get_reset_token()  # 'get_reset_token()' is found in 'models.py'
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external=True)} If you did not make this request then simply ignore this email and no changes will be made.'''  # '_external=True' means it should return an absolute url and not a relative url

    mail.send(msg)  # this sends the message to the user using the stated mail in '__init__.py'
    print(msg)  # this displays the message and its content in the cli(command line interface)


