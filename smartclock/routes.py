from smartclock import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from smartclock.forms import RegistrationForm, LoginForm
from smartclock.models import User, Timesheet, user_schema, users_schema, timesheet_schema, timesheets_schema
from smartclock.functions import check_password, hash_password
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime



@app.route("/")
@app.route("/home")
def home():
    return render_template('public/home.html')


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
    if current_user.is_admin:
        users = User.query.filter_by(is_admin = False).all()
        return render_template('auth/admin/admin-dash.html', title='Dashboard',  users = users)
    else:
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



"""
    REST API Implementation
"""
# get all users
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result =  users_schema.dump(all_users)
    return jsonify(result)

# get a user by its username
@app.route('/api/v1/users/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message':'user does not exist'})
    return user_schema.jsonify(user)

# get all timesheets
@app.route('/api/v1/timesheets', methods=['GET'])
def get_timesheets():
    all_timesheets = Timesheet.query.all()
    result =  timesheets_schema.dump(all_timesheets)
    return jsonify(result)


# get a timesheet by its id
@app.route('/api/v1/timesheets/<int:id>', methods=['GET'])
def get_timesheet(id):
    timesheet = Timesheet.query.get_or_404(id)
    if not timesheet:
        return jsonify({'message':'timesheet does not exist'})
    return timesheet_schema.jsonify(timesheet)


# post a timesheet by its id
@app.route('/api/v1/timesheets/', methods=['POST'])
def post_timesheet():
    date = datetime.utcnow()
    clock_in_time = datetime.utcnow()
    clock_out_time = datetime.now()
    is_clocked_in = request.json['is_clocked_in']
    user_id = request.json['user_id']
    timesheet = Timesheet(date = date, clock_in_time=clock_in_time, clock_out_time=clock_out_time, is_clocked_in=is_clocked_in, user_id=user_id)
    db.session.add(timesheet)
    db.session.commit()
    return timesheet_schema.jsonify(timesheet)
