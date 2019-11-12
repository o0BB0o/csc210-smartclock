from smartclock import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from smartclock.forms import RegistrationForm, LoginForm
from smartclock.models import User
from smartclock.functions import check_password, hash_password
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    # in case, if user is already logged in, it will redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form  = RegistrationForm()

    if(form.validate_on_submit()):

        hashed_password = hash_password(password = form.password.data)
        user = User(username = form.username.data, password = hashed_password, email = form.email.data)

        db.session.add(user)
        db.session.commit( )

        flash("Successfully signed up, try to login now!")

        return redirect(url_for('home'))

    return render_template('signup.html', form=form, title='Sign Up')

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password(password = form.password.data, hash_ = user.password):

            login_user(user, remember=form.remember.data)

            flash("Welcome back!")

            # for the anonymous users who try to reach login_required pages will firstly lead them to this login page,
            # remembers that login_required page and redirects them back after they've logged in
            # else they go to home page

            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')



    return render_template('login.html', form = form, title='Log in')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    return  render_template('profile.html', title='My Profile')


"""
    Restful API Implementation
    
"""
@app.route("/api/v1/users/")
def get_users():
    users = User.query.all()
    return jsonify({"posts": [user.to_json() for user in users]})

@app.route("/api/v1/post/<int:id>")
def get_post(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user.to_json())


