from models import db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
# Add new data
user_1 = User(first_name="joel", last_name="burton", image_url="https://www.opticalexpress.co.uk/media/1064/man-with-glasses-smiling-looking-into-distance.jpg")
user_2 = User(first_name="alan", last_name="alda", image_url="https://expertphotography.b-cdn.net/wp-content/uploads/2018/10/cool-profile-picture-natural-light.jpg")
user_3 = User(first_name="jane", last_name="smith", image_url="https://images.pexels.com/photos/1704488/pexels-photo-1704488.jpeg")
user_4 = User(first_name="charles", last_name="moore", image_url="https://keenthemes.com/preview/metronic/theme/assets/pages/media/profile/profile_user.jpg")
# Add new objects to session, so they'll persist
db.session.add(user_1)
db.session.add(user_2)
db.session.add(user_3)
db.session.add(user_4)
# Commit--otherwise, this never gets saved!
db.session.commit()


# If table isn't empty, empty it
Post.query.delete()
# Add new data
data_1 = Post(title="first post!", content="post content 1...!", created_at="01/01/2022 12:00:00", user_id="1")
data_2 = Post(title="yet another post", content="post content 2...!", created_at="01/01/2022 12:00:00", user_id="1")
data_3 = Post(title="flask is awesome", content="post content 3...!", created_at="01/01/2022 12:00:00", user_id="1")
# Add new objects to session, so they'll persist
db.session.add(data_1)
db.session.add(data_2)
db.session.add(data_3)
# Commit--otherwise, this never gets saved!
db.session.commit()