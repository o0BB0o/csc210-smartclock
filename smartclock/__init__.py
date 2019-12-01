from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# variables
database_name = 'smartclock.db'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba212'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+database_name

db = SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.login_view = 'login'

"""
By default, when a user attempts to access a login_required view without being logged in,
Flask-Login will flash a message and redirect them to the log in view.
(If the login view is not set, it will abort with a 401 error.)
The name of the log in view can be set as LoginManager.login_view.
"""

from smartclock import routes
