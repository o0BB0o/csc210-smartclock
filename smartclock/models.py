from smartclock import app, db, ma, login_manager
from flask_login import UserMixin
from smartclock.functions import tableDoesNotExist
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer \
as Serializer

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
    confirmed = db.Column(db.Boolean, default=False) # False == Email not authenticated --> True == Email authenticated


    # admin's privileges
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # relationships
    timesheets = db.relationship("Timesheet", backref="user")

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def generate_reset_token(self, expiration=3600):
        s = Serializer(app.config["SECRET_KEY"], expiration)
        return s.dumps({"reset": self.id}).decode("utf-8")

    def confirmresettoken(self, token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception:
            return False
        if data.get("reset") != self.id:
            return False
        return True

    def confirm(self, token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.commit()
        return True

class Timesheet(db.Model):
    # required
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    clock_in_time = db.Column(db.DateTime)
    clock_out_time = db.Column(db.DateTime)
    is_clocked_in = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_approved', 'is_admin', 'confirmed', 'timesheets')

class TimesheetSchema(ma.Schema):
    class Meta:
        model = Timesheet
        fields = ('id', 'date', 'clock_in_time', 'clock_out_time', 'is_clocked_in', 'user_id')

timesheet_schema = TimesheetSchema()
timesheets_schema = TimesheetSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

if tableDoesNotExist(User.__tablename__):
    db.drop_all()
    db.create_all()

