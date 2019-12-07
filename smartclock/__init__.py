from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail

database_name = 'smartclock.db'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba212'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_name
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'testsmartclock@gmail.com'
app.config['MAIL_PASSWORD'] = 'Rochester2019'
app.config['MAIL_DEFAULT_SENDER'] = 'testsmartclock@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)


login_manager=LoginManager(app)
login_manager.login_view = 'login'


from smartclock.routes import *
from smartclock.apis import *


