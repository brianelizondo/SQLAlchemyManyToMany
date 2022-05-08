"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from models import Tag, db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcd1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 Error Page"""
    return render_template('404.html'), 404

@app.route("/")
def home_page():
    """Homepage that shows the 5 most recent posts"""
    posts = Post.query.order_by(desc(Post.id)).limit(5).all()
    
    for post in posts:
        date_object = datetime.strptime(str(post.created_at), "%Y-%m-%d %H:%M:%S")
        post.created_at = date_object.strftime("%a %b %-d %Y, %-I:%M %p")

    return render_template("home.html", posts=posts)


# Routes for Users
@app.route("/users")
def show_users():
    """
    Show all users
    Links to view the detail page for the user and a link to the add-user form
    """
    users = User.query.order_by(User.last_name).all()
    return render_template("users.html", users=users)

@app.route("/users/new")
def add_user_form():
    """
    Show an add form for users
    """
    return render_template("user_new.html")


@app.route("/users/new", methods=["POST"])
def add_user_process():
    """
    Process the add form, adding a new user and going back to /users
    """
    user_first_name = request.form["first_name"].lower()
    user_last_name = request.form["last_name"].lower()
    user_image_url = request.form["image_url"].lower()

    valid_fields = True
    if len(user_first_name) == 0:
        valid_fields = False
        flash("Please enter your first name")
    if len(user_last_name) == 0:
        valid_fields = False
        flash("Please enter your last name")
    if len(user_image_url) == 0:
        valid_fields = False
        flash("Please provide an image url")

    if valid_fields:
        new_user = User(first_name=user_first_name, last_name=user_last_name, image_url=user_image_url)
        db.session.add(new_user)
        db.session.commit()
        flash("The user was added successfully")
        return redirect("/users")
    else:
        return redirect("/users/new")


@app.route("/users/<int:user_id>")
def users_details(user_id):
    """
    Show information about the given user.
    Have a button to get to their edit page, and to delete the user.
    """
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("user_details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def users_edit(user_id):
    """
    Show the edit page for a user.
    Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
    """
    user = User.query.get(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def users_edit_process(user_id):
    """
    Process the edit form, returning the user to the /users page.
    """
    update_user = User.query.get(user_id)
    user_first_name = request.form["first_name"].lower()
    user_last_name = request.form["last_name"].lower()
    user_image_url = request.form["image_url"].lower()

    valid_fields = True
    if len(user_first_name) == 0:
        valid_fields = False
        flash("Please enter your first name")
    if len(user_last_name) == 0:
        valid_fields = False
        flash("Please enter your last name")
    if len(user_image_url) == 0:
        valid_fields = False
        flash("Please provide an image url")

    if valid_fields:
        update_user.first_name = user_first_name
        update_user.last_name = user_last_name
        update_user.image_url = user_image_url
        db.session.add(update_user)
        db.session.commit()
        flash("The user was successfully modified")
        return redirect("/users")
    else:
        return redirect("/users/new")


@app.route("/users/<int:user_id>/delete", methods=["GET", "POST"])
def users_delete(user_id):
    """
    Delete the user.
    """
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash("The user was successfully deleted")
    return redirect("/users")


# Routes for Posts
@app.route("/users/<int:user_id>/posts/new")
def add_post_form(user_id):
    """
    Show form to add a post for that user
    """
    user = User.query.get(user_id)
    tags = Tag.query.order_by('name').all()
    return render_template("post_new.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post_process(user_id):
    """
    Handle add form; add post and redirect to the user detail page
    """
    post_title = request.form["post_title"]
    post_content = request.form["post_content"]
    post_created = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    tags_id = [int(id) for id in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tags_id)).all()

    valid_fields = True
    if len(post_title) == 0:
        valid_fields = False
        flash("Please enter the post title")
    if len(post_content) == 0:
        valid_fields = False
        flash("Please enter the post content")

    if valid_fields:
        new_post = Post(title=post_title, content=post_content, created_at=post_created, user_id=user_id, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        flash("The post was added successfully")
        return redirect(f'/users/{ user_id }')
    else:
        return redirect(f'/users/{ user_id }/posts/new')


@app.route("/posts/<int:post_id>")
def posts_details(post_id):
    """
    Show a post.
    Show buttons to edit and delete the post.
    """
    post = Post.query.get(post_id)
    date_object = datetime.strptime(str(post.created_at), "%Y-%m-%d %H:%M:%S")
    post.created_at = date_object.strftime("%a %b %-d %Y, %-I:%M %p")
    
    return render_template("post_details.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def posts_edit(post_id):
    """
    Show form to edit a post, and to cancel (back to user page).
    """
    post = Post.query.get(post_id)
    tags = Tag.query.order_by('name').all()
    return render_template("post_edit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def posts_edit_process(post_id):
    """
    Handle editing of a post. Redirect back to the post view.
    """
    update_post = Post.query.get(post_id)
    post_title = request.form["post_title"]
    post_content = request.form["post_content"]

    tags_id = [int(id) for id in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tags_id)).all()

    valid_fields = True
    if len(post_title) == 0:
        valid_fields = False
        flash("Please enter the post title")
    if len(post_content) == 0:
        valid_fields = False
        flash("Please enter the post content")

    if valid_fields:
        update_post.title = post_title
        update_post.content = post_content
        update_post.tags = tags
        db.session.add(update_post)
        db.session.commit()
        flash("The post was successfully modified")
        return redirect(f'/posts/{ post_id }')
    else:
        return redirect(f'/posts/{ post_id }/edit')

@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def posts_delete(post_id):
    """
    Delete the post.
    """
    delete_post = Post.query.get(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash("The post was successfully deleted")
    return redirect(f'/users/{ delete_post.user_id }')


# Routes for Tags
@app.route("/tags")
def show_tagss():
    """
    Lists all tags, with links to the tag detail page
    """
    tags = Tag.query.order_by('name').all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def tags_details(tag_id):
    """
    Show detail about a tag. Have links to edit form and to delete
    """
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template("tag_details.html", tag=tag, posts=posts)

@app.route("/tags/new")
def add_tag_form():
    """
    Shows a form to add a new tag
    """
    posts = Post.query.all()
    return render_template("tag_new.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def add_tag_process():
    """
    Process add form, adds tag, and redirect to tag list
    """
    tag_name = request.form["name"].lower()

    posts_id = [int(id) for id in request.form.getlist("posts")]
    posts_list = Post.query.filter(Post.id.in_(posts_id)).all()

    valid_fields = True
    if len(tag_name) == 0:
        valid_fields = False
        flash("Please enter a name for the tag")

    if valid_fields:
        new_tag = Tag(name=tag_name, posts=posts_list)
        db.session.add(new_tag)
        db.session.commit()
        flash("The tag was added successfully")
        return redirect("/tags")
    else:
        return redirect("/tags/new")

@app.route("/tags/<int:tag_id>/edit")
def tags_edit(tag_id):
    """
    Show edit form for a tag
    """
    tag = Tag.query.get(tag_id)
    posts = Post.query.all()
    return render_template("tag_edit.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def tags_edit_process(tag_id):
    """
    Process edit form, edit tag, and redirects to the tags list
    """
    update_tag = Tag.query.get(tag_id)
    tag_name = request.form["name"]
    posts_id = [int(id) for id in request.form.getlist("posts")]
    posts_list = Post.query.filter(Post.id.in_(posts_id)).all()

    valid_fields = True
    if len(tag_name) == 0:
        valid_fields = False
        flash("Please enter a name for the tag")

    if valid_fields:
        update_tag.name = tag_name
        update_tag.posts = posts_list
        db.session.add(update_tag)
        db.session.commit()
        flash("The tag was successfully modified")
        return redirect(f'/tags/{ tag_id }')
    else:
        return redirect(f'/tags/{ tag_id }/edit')

@app.route("/tags/<int:tag_id>/delete", methods=["GET", "POST"])
def tags_delete(tag_id):
    """
    Delete the tag.
    """
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    flash("The tag was successfully deleted")
    return redirect("/tags")