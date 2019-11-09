from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired])
    email = StringField('Email', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired, Length(min=5)])
    confirm_password = StringField('Confirm Password', validators=[DataRequired, EqualTo('password')])
    submit = SubmitField()

    def validate_username(self):
        pass
    def validate_email(self):
        pass

class LoginForm(FlaskForm):
    username = StringField()
    email = StringField()
    password = StringField()
    confirm_password = StringField()



