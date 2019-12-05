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

    # admin's privileges
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)


    # relationships
    timesheets = db.relationship("Timesheet", backref="user")
    schedules = db.relationship("Schedule", backref="user")


    def __repr__(self):
        return '<User %r>' % self.username

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_approved', 'is_admin', 'timesheets', 'schedules')

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.String(20))
    start_time = db.Column(db.String(20))
    end_time = db.Column(db.String(20))
    hourly_rate = db.Column(db.Float, default=12.75)
    user_id = db.Column(db.Integer(),
                        db.ForeignKey("user.id"))
class ScheduleSchema(ma.Schema):
    class Meta:
        model = Schedule
        fields = ('id', 'week_day', 'start_time', 'end_time', 'hourly_rate', 'user_id')

schedule_schema = ScheduleSchema(strict=True)
schedules_schema = ScheduleSchema(many=True, strict=True)


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
