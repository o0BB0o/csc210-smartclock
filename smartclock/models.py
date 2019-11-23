from smartclock import db, login_manager
from flask_login import UserMixin
from smartclock.functions import tableDoesNotExist, hash_password
from datetime import datetime

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
    # required

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    is_supervisor = db.Column(db.Boolean, default=False)
    hourly_rate = db.Column(db.Float, default=12.75)

    # optional
    #
    # first_name = db.Column(db.String(120), nullable=True)
    # last_name = db.Column(db.String(120), nullable=True)
    # phone_number = db.Column(db.String(120), nullable=True)
    # created_at = db.Column(db.DateTime, default=datetime.now)

    # beyond
    #
    # email_auth_token = db.Column(db.Text, nullable=True)
    # is_authenticated = db.Column(db.Boolean, default=False)

    # relationships

    timesheets = db.relationship("Timesheet", backref="user")

    def __repr__(self):
        return '<User %r>' % self.username


class Timesheet(db.Model):
    # required
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    # date_submitted = db.Column(db.DateTime, nullable=True, default=None)
    clock_in_time = db.Column(db.DateTime, nullable=False)
    clock_out_time = db.Column(db.DateTime, nullable=True)

    # is_clocked_in = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"))


if tableDoesNotExist(User.__tablename__):
    db.drop_all()
    db.create_all()

# that is how we use it!
# ts_1 = Timesheet(datetime.utcnow(), datetime.utcnow(), datetime.now())
# user_1 = User(username="islomzhan", password="tests", email="the@database.comm", timesheets=[ts_1])
#
# db.session.add_all([ts_1])
# db.session.add(user_1)
# db.session.commit()
