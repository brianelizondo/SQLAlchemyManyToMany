"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Create a User model for SQLAlchemy"""

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

     __tablename__ = "post"

     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     title = db.Column(db.String(100), nullable=False)
     content = db.Column(db.Text, nullable=False)
     created_at = db.Column(db.DateTime, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

     # users = db.relationship('User', backref='posts')
     users = db.relationship('User')