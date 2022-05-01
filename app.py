"""Blogly application."""

from crypt import methods
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcd1234"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()

@app.route("/")
def home_page():
    """Redirect to list of users"""
    return redirect("/users")

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
    return render_template("new_user.html")


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
    return render_template("user_details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def users_edit(user_id):
    """
    Show the edit page for a user.
    Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
    """
    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)


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