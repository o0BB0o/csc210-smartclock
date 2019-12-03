from smartclock import app, db
from flask import render_template, redirect, url_for, flash, request
from smartclock.forms import RegistrationForm, LoginForm
from smartclock.models import User
from smartclock.functions import check_password, hash_password
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home():
    return render_template('public/home.html')

@app.route("/email_auth")
def email_auth():
     return render_template('auth/email_auth.html')

@app.route("/about")
def about():
    return render_template('public/about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # in case, if user is already logged in, it will redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = hash_password(password=form.password.data)
        user = User(username=form.username.data, password=hashed_password, email=form.email.data,
                    last_name=form.lname.data, first_name=form.fname.data)

        db.session.add(user)
        db.session.commit()

        flash("You have successfully created your account, login now!", "success")

        return redirect(url_for('home'))

    return render_template('public/register.html', form=form, title='Register')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password(password=form.password.data, hash_=user.password):
            login_user(user, remember=form.remember.data)
            flash("Welcome back!", "info")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('public/login.html', form=form, title='Log in')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('auth/dashboard.html', title='Dashboard')

@app.route("/confirm/<string:token>") # EMAIL AUTHENTICATION
@login_required
def confirm(token):
    if current_user.confirmed:
        pass
    elif current_user.confirm(token):
        flash("Your account is now confirmed")
    else:
        flash("Your confirmation link is invalid or has expired")
    return redirect(url_for("index"))

@app.route("/settings")
@login_required
def settings():
    return render_template('auth/settings.html', title='Settings')

@app.route("/view")
@login_required
def view():
    return render_template('auth/view.html', title='View Timesheets')