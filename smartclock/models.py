from smartclock import db, login_manager
from flask_login import UserMixin
from smartclock.functions import tableDoesNotExist

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
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

if tableDoesNotExist(User.__tablename__):
    db.drop_all()
    db.create_all()