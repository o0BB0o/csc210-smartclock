from smartclock import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from smartclock.forms import RegistrationForm, LoginForm, WeekTimeForm
from smartclock.models import User, Timesheet, Schedule, user_schema, users_schema, timesheet_schema, timesheets_schema, schedule_schema
from smartclock.functions import check_password, hash_password
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import and_


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
        return render_template('auth/admin/admin-dash.html', title='Dashboard')
    else:
        return render_template('auth/dashboard.html', title='Dashboard')

@app.route("/assign/<string:username>", methods=["GET"])
@login_required
def modify(username):
    if current_user.is_admin:
        if username:
            user = User.query.filter_by(username=username).first()
            if user:

                form = LoginForm()
                if form.validate_on_submit():
                    # username=form.username.data, email=form.email.data
                    schedule = Schedule()
                    user.schedules.append(schedule)
                    db.session.commit()
                    flash("You have successfully added new time!", "success")
                    return redirect(url_for('modify', username=user.username))
                return render_template('auth/admin/user-view.html', selected_user=user, title='Manage Users')
            else:
                flash_text = 'User with that username selected was not found, go back and try again!'
                flash(flash_text,'warning')
                return render_template('auth/admin/admin-dash.html', title='Admin ')
        else:
            return render_template('auth/admin/admin-dash.html', title="Admin ")
    else:
        return render_template('auth/dashboard.html', title='Dashboard')


# @app.route("/confirm/<string:token>") # EMAIL AUTHENTICATION
# @login_required
# def confirm(token):
#     if current_user.confirmed:
#         pass
#     elif current_user.confirm(token):
#         flash("Your account is now confirmed")
#     else:
#         flash("Your confirmation link is invalid or has expired")
#     return redirect(url_for("index"))

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

"""
    --> CREATE methods | REST API 
"""
# create a timesheet
@app.route('/api/v1/timesheet', methods=['POST'])
def create_timesheet():
    date = request.json['date']
    todays_date = datetime.now().date()
    clock_in_time = request.json['clock_in_time']
    clock_out_time = request.json['clock_out_time']
    is_clocked_in = request.json['is_clocked_in']
    user_id = request.json['user_id']
    new_timesheet = Timesheet(date=date, todays_date=todays_date, clock_in_time=clock_in_time,
                              clock_out_time=clock_out_time, is_clocked_in=is_clocked_in, user_id=user_id)
    db.session.add(new_timesheet)
    db.session.commit()
    return timesheet_schema.jsonify(new_timesheet)


# create a user
@app.route('/api/v1/user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    hashed_password = hash_password(password)
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    is_approved = request.json['is_approved']
    is_admin = request.json['is_admin']
    num_of_days_missing = request.json['num_of_days_missing']
    num_of_days_left_early = request.json['num_of_days_left_early']
    num_of_days_coming_late = request.json['num_of_days_coming_late']
    timesheets = request.json['timesheets']  # if nothing place []
    schedules = request.json['schedules']  # if nothing place []
    date = request.json['created_at']
    created_at = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    new_user = User(username=username, created_at=created_at, timesheets=timesheets, schedules=schedules,
                    num_of_days_coming_late=num_of_days_coming_late, num_of_days_left_early=num_of_days_left_early,
                    num_of_days_missing=num_of_days_missing, first_name=first_name, last_name=last_name, email=email,
                    is_admin=is_admin, is_approved=is_approved, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

"""
    --> GET methods | REST API 
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

"""
    --> PATCH methods | REST API 
    
    Why not put because for now we don't need it since, with patch we can change what we want, without affecting 
    the rest of the fields in our Model, because for put we need to list all fields that are actually in Model, and 
    we should redefine some of them, if we want to keep them.
"""


# patch a user to clock in
@app.route('/api/v1/user/<int:uid>', methods=['PATCH'])
def clock_in_user(uid):

    user = User.query.filter_by(username=uid).first()

    if user is not None and user.is_approved and not user.is_admin:
        todays_date = datetime.now().date()
        wanted_row = Timesheet.query.filter_by(and_(user_id = user.id, todays_date = todays_date)).first()

        if todays_date == wanted_row.todays_date:
            if wanted_row.is_clocked_in:
                return user_schema.jsonify(user)
            else:
                wanted_row.is_clocked_in = True
                wanted_row.todays_date = datetime.now().date()
                wanted_row.clock_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.session.commit()
                return user_schema.jsonify(user)
        else:
            # that means that the user is on a new day to work
            # now we will create a new timesheet row which will let to clock in and stamp its time
            # then we will add it to the db session
            new_time_row = Timesheet(is_clocked_in=True, todays_date = datetime.now().date(), clock_in_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id = user.id)
            db.session.add(new_time_row)
            db.session.commit()
            return user_schema.jsonify(user)

    if user is None:
        return jsonify({'message':'does not exist'})
    if not user.is_approved:
        return jsonify({'message':'user is not yet approved'})
    if user.is_admin:
        return jsonify({'message':'user is admin'})

    return jsonify({'message':'some_other_errors'})

# patch a user to clock out
@app.route('/api/v1/users/<username>/out', methods=['PATCH'])
def clock_out_user(username):

    user = User.query.filter_by(username=username).first()

    if user is not None and user.is_approved and not user.is_admin:
        todays_date = datetime.now().date()
        wanted_row = Timesheet.query.filter_by(and_(user_id = user.id, todays_date = todays_date)).first()

        if todays_date == wanted_row.todays_date:
            if wanted_row.is_clocked_in:
                wanted_row.is_clocked_in = False
                wanted_row.clock_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.session.commit()
                return user_schema.jsonify(user)
            else:
                return jsonify({'message':'it is already clocked out'})

    if user is None:
        return jsonify({'message':'does not exist'})
    if not user.is_approved:
        return jsonify({'message':'user is not yet approved'})
    if user.is_admin:
        return jsonify({'message':'user is admin'})

    return jsonify({'message':'some_other_errors'})


"""
    --> DELETE methods | REST API 
    Why not put because for now we don't need it since, with patch we can change what we want, without affecting 
    the rest of the fields in our Model, because for put we need to list all fields that are actually in Model, and 
    we should redefine some of them, if we want to keep them.
"""

# delete a user by id
@app.route('/api/v1/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    """

    Before deleting a user, we must check to its child models, if they exist, we should remove them, then remove itself.

    """
    user_to_be_deleted = User.query.filter_by(id=id).first()
    ts_of_that_user = Timesheet.query.filter_by(user_id=user_to_be_deleted.id).all()
    sl_of_that_user = Schedule.query.filter_by(user_id=user_to_be_deleted.id).all()

    if not user_to_be_deleted:
        return jsonify({'message':'user does not exist'})

    if len(ts_of_that_user) > 0:
        db.session.delete(ts_of_that_user)

    if len(sl_of_that_user) > 0:
        db.session.delete(sl_of_that_user)

    db.session.delete(user_to_be_deleted)
    db.session.commit()
    return user_schema.jsonify(user_to_be_deleted)


@app.route('/api/v1/schedule/<int:id>', methods=['DELETE'])
def del_schedule(id):
    sl = Schedule.query.filter_by(id = id).first()
    if not sl:
        return jsonify({'message':'grabber of the first schedule, will remove the first'})
    db.session.delete(sl)
    db.session.commit()
    return schedule_schema.jsonify(sl)

@app.route('/api/v1/timesheet/<int:id>', methods=['DELETE'])
def del_timesheet(id):
    ts = Timesheet.query.filter_by(id = id).first()
    if not ts:
        return jsonify({'message':'timesheet does not exist'})
    db.session.delete(ts)
    db.session.commit()
    return timesheet_schema.jsonify(ts)







