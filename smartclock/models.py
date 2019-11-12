from smartclock import db, login_manager, database_name
from flask_login import UserMixin
import os, sqlite3

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



# custom method to handle the database if it doesn't exist
appdir = os.path.abspath(os.path.dirname(__file__))
database_location = os.path.join(appdir, database_name)

def database_exists():
    return os.path.exists(database_location)

def checkTableExists(tablename):
    con = sqlite3.connect(database_location)
    c = con.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s' " % tablename)
    if c.fetchone()[0] == 1:
        c.close()
        # Table exists
        return True

    c.close()
    return False


if database_exists is False or checkTableExists(User.__tablename__) is False:
    db.drop_all()
    db.create_all()
