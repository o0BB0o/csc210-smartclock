from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail

database_name = 'smartclock.db'

app = Flask(__name__)

from smartclock.config import *

db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)


login_manager=LoginManager(app)
login_manager.login_view = 'login'


from smartclock.routes import *
from smartclock.apis import *


