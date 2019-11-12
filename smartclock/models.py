from smartclock import db, login_manager, app
from flask_login import UserMixin
from smartclock.functions import tableDoesNotExist
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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

    confirmed = db.Column(db.Boolean(), default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):

        s = Serializer(app.config["SECRET_KEY"])

        try:
            data = s.loads(token.encode("utf-8"))
        except Exception:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

if tableDoesNotExist(User.__tablename__):
    db.drop_all()
    db.create_all()