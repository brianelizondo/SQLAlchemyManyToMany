from app import app
from models import db, User

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add new data
data_1 = User(first_name='joel', last_name="burton", image_url="profile.jpg")
data_2 = User(first_name='alan', last_name="alda")
data_3 = User(first_name='jane', last_name="smith")

# Add new objects to session, so they'll persist
db.session.add(data_1)
db.session.add(data_2)
db.session.add(data_3)

# Commit--otherwise, this never gets saved!
db.session.commit()
