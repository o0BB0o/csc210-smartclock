from smartclock import db, login_manager, database_name
from flask_login import UserMixin
import os

"""
Learn more here:
https://flask-login.readthedocs.io/en/latest/ 

You will need to provide a user_loader callback. 
This callback is used to reload the user object from the user ID stored in the session. 
It should take the unicode ID of a user, and return the corresponding user object. 
"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# custom method to handle the database if it doesn't exist
def db_not_exists():
    appdir = os.path.abspath(os.path.dirname(__file__))
    return not os.path.exists(os.path.join(appdir, database_name))

if db_not_exists():
    print("it doesn't exist")
    db.drop_all()
    db.create_all()
else:
    print("it exists")
