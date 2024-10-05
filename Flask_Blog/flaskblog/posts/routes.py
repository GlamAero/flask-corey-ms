from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog.models import Post
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.posts.forms import PostForm


# the below creates the posts's blueprint
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():  # this creates a new post for the current_user
    form = PostForm()  
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):  # this is used to view a post and its full content
    post = Post.query.get_or_404(post_id)  # 'get_or_404' means to get the post object(post_id) or return a 404 error if the post_id does not exist
    return render_template('post.html', title=post.title, post=post)
    

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):  # this is used by the current_user to update the post the current_user created
    post = Post.query.get_or_404(post_id)  # 'get_or_404' means to get the post object(post_id) or return a 404 error if the post_id does not exist
    if post.author != current_user:
        abort(403)  # this prevents a current_user who did not create the post to update it
    
    form = PostForm()
    if form.validate_on_submit():
        # this saves the inputed title and content into the database
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    
    # filling the form with 'title' and 'content' data by default as follows so as to edit/update:
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template("create_post.html", title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # 'get_or_404' means to get the post object(post_id) or return a 404 error if the post_id does not exist
    if post.author != current_user:
        abort(403)  # this prevents a current_user who did not create the post to update it
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


