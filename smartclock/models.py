from smartclock import db, ma, login_manager
from flask_login import UserMixin
from smartclock.functions import tableDoesNotExist
from datetime import datetime

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
    def __repr__(self):
        return '<User %r>' % self.username

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

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_approved', 'is_admin', 'timesheets')

class TimesheetSchema(ma.Schema):
    class Meta:
        model = Timesheet
        fields = ('id', 'date', 'clock_in_time', 'clock_out_time', 'is_clocked_in', 'user_id')

timesheet_schema = TimesheetSchema(strict=True)
timesheets_schema = TimesheetSchema(many=True, strict=True)
user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

if tableDoesNotExist(User.__tablename__):
    db.drop_all()
    db.create_all()

