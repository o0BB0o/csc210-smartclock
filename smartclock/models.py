from smartclock import db, ma, login_manager
from flask_login import UserMixin
from smartclock.functions import tableDoesNotExist
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.Text)
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    num_of_days_missing =  db.Column(db.Integer, default=0)
    num_of_days_left_early =  db.Column(db.Integer, default=0)
    num_of_days_coming_late =  db.Column(db.Integer, default=0)

    # admin's privileges
    approved_on = db.Column(db.DateTime, nullable=True)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    hourly_rate = db.Column(db.Float, default=12.75, nullable=True)

    # beyond
    # email_auth_token = db.Column(db.Text, nullable=True)
    # is_authenticated = db.Column(db.Boolean, default=False)

    # relationships
    timesheets = db.relationship("Timesheet", backref="user")

    def __repr__(self):
        return '<User %r>' % self.username

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_approved', 'created_at', 'num_of_days_missing', 'num_of_days_left_early', 'num_of_days_coming_late', 'is_admin', 'hourly_rate')

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)


class Timesheet(db.Model):
    # required
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    todays_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    clock_in_time = db.Column(db.DateTime, nullable=False)
    clock_out_time = db.Column(db.DateTime, nullable=True)
    is_clocked_in = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"))

class TimesheetSchema(ma.Schema):
    class Meta:
        model = Timesheet
        fields = ('id', 'date', 'clock_in_time', 'clock_out_time', 'is_clocked_in', 'user_id')

timesheet_schema = TimesheetSchema(strict=True)
timesheets_schema = TimesheetSchema(many=True, strict=True)




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
