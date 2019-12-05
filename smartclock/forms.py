from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from smartclock.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("The username exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("The email exists")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class WeekTimeForm(FlaskForm):
    week = SelectField('Week', choices=[('Mon','Monday'), ('Tue','Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'),
                                        ('Fri', 'Friday'), ('Sat', 'Saturday'), ('Sun', 'Sunday')], validators=[DataRequired()])
    start_time = TimeField('Start Time', format="%H:%M", validators=[DataRequired()])
    end_time = TimeField('End Time', format="%H:%M", validators=[DataRequired()])
    submit = SubmitField('Save')


