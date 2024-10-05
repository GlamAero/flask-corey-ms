from flask import Blueprint, render_template, request
from flaskblog.models import Post


# the below creates the main's blueprint
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # 'page' here means the page number(not number of pages)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # 'order_by(Post.date_posted.desc())' means to display the objects in descending order on date bases, with the latest post appearing as first adn others fall under it. 'per_page' here means the number of items(content) per page.
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title='About')