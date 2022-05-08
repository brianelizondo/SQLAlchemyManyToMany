"""Models for Blogly."""

from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Create a User model for SQLAlchemy"""
    def __repr__(self):
        """Show info about User"""
        u = self
        return f"<User - ID: {u.id} Full_Name: {u.full_name}>"

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=None)

    posts = db.relationship('Post', cascade="all, delete", passive_deletes=True)

    def get_full_name(self):
        """Get the user full name"""
        return f"{self.first_name} {self.last_name}"

    full_name = property(
        fget = get_full_name
    )


class Post(db.Model):
     """Create a Post model for SQLAlchemy"""
     def __repr__(self):
        """Show info about Post"""
        p = self
        return f"<Post - ID: {p.id} Title: {p.title}>"

     __tablename__ = "post"

     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     title = db.Column(db.String(100), nullable=False)
     content = db.Column(db.Text, nullable=False)
     created_at = db.Column(db.DateTime, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

     # users = db.relationship('User', backref='posts')
     users = db.relationship('User')
     tags = db.relationship('Tag', secondary='posts_tags', backref='posts', cascade="all, delete", passive_deletes=True)


class PostTag(db.Model):
    """Create a PostTag model for SQLAlchemy"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    

class Tag(db.Model):
    """Create a Tag model for SQLAlchemy"""
    def __repr__(self):
        """Show info about Tag"""
        t = self
        return f"<Tag - ID: {t.id} name: {t.name}>"

    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)