from smartclock import app, db, mail
from flask import render_template, redirect, url_for, flash, request, jsonify
from smartclock.forms import RegistrationForm, LoginForm, EmailPasswordForm, PasswordResetForm
from smartclock.models import User, Timesheet, user_schema, users_schema, timesheet_schema, timesheets_schema
from smartclock.functions import check_password, hash_password
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import and_
from smartclock.email import send_email, send_email2



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

        if user and check_password(password=form.password.data, hash_=user.password) and user.confirmed is True:
            login_user(user, remember=form.remember.data)
            flash("Welcome back!", "info")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        elif user and check_password(password = form.password.data, hash_ = user.password) and user.confirmed is False:
            flash("User account pending --> please check email")
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
        return render_template('auth/admin/admin.html', title='Dashboard')
    else:
        return render_template('auth/dashboard.html', title='Dashboard')

@app.route("/dashboard/<string:username>", methods=["GET"])
@login_required
def modify(username):
    if current_user.is_admin:
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                return render_template('auth/admin/user.html', selected_user=user, title='Manage Users')
            else:
                flash('There is no user with that username!','warning')
                return render_template('auth/admin/admin.html', title='Admin ')
        else:
            return render_template('auth/admin/admin.html', title="Admin ")
    else:
        return render_template('auth/dashboard.html', title='Dashboard')

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
# @app.route('/api/v1/timesheet', methods=['POST'])
# def create_timesheet():
#     date = request.json['date']
#     todays_date = datetime.now().date()
#     clock_in_time = request.json['clock_in_time']
#     clock_out_time = request.json['clock_out_time']
#     is_clocked_in = request.json['is_clocked_in']
#     user_id = request.json['user_id']
#     new_timesheet = Timesheet(date=date, todays_date=todays_date, clock_in_time=clock_in_time,
#                               clock_out_time=clock_out_time, is_clocked_in=is_clocked_in, user_id=user_id)
#     db.session.add(new_timesheet)
#     db.session.commit()
#     return timesheet_schema.jsonify(new_timesheet)


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
    timesheets = request.json['timesheets']  # if nothing place []

    new_user = User(username=username, timesheets=timesheets, first_name=first_name, last_name=last_name, email=email,
                    is_admin=is_admin, is_approved=is_approved, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# # update a user
# @app.route('/api/v1/users/<username>', methods=['PUT'])
# def put_user(username):
#     user = User.query.filter_by(username=username).first()
#     username = request.json['username']
#     password = request.json['password']
#     hashed_password = hash_password(password)
#     first_name = request.json['first_name']
#     last_name = request.json['last_name']
#     email = request.json['email']
#     is_approved = request.json['is_approved']
#     is_admin = request.json['is_admin']
#     timesheets = request.json['timesheets']  # if nothing place []
#
#     user.username=username
#     user.timesheets=timesheets
#     user.first_name=first_name
#     user.last_name=last_name
#     user.email=email
#     user.is_admin=is_admin
#     user.is_approved=is_approved
#     user.password=hashed_password
#
#     db.session.commit()
#
#     return user_schema.jsonify(user)

# patch approve
@app.route('/api/v1/users/approve/<username>', methods=['PATCH'])
def patch_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        is_approved = request.json['is_approved']
        user.is_approved=is_approved
        db.session.commit()
        return user_schema.jsonify(user)
    else:
        return jsonify("message", "error")

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

# # get all timesheets
# @app.route('/api/v1/timesheets', methods=['GET'])
# def get_timesheets():
#     all_timesheets = Timesheet.query.all()
#     result =  timesheets_schema.dump(all_timesheets)
#     return jsonify(result)
#
#
# # get a timesheet by its id
# @app.route('/api/v1/timesheets/<int:id>', methods=['GET'])
# def get_timesheet(id):
#     timesheet = Timesheet.query.get_or_404(id)
#     if not timesheet:
#         return jsonify({'message':'timesheet does not exist'})
#     return timesheet_schema.jsonify(timesheet)

"""
    --> DELETE methods | REST API 
    Why not put because for now we don't need it since, with patch we can change what we want, without affecting 
    the rest of the fields in our Model, because for put we need to list all fields that are actually in Model, and 
    we should redefine some of them, if we want to keep them.
"""

# delete a user by id
@app.route('/api/v1/user/<username>', methods=['DELETE'])
def delete_user(username):
    """

    Before deleting a user, we must check to its child models, if they exist, we should remove them, then remove itself.
    To avoid database crash, since, its children have its id linked

    """
    user_to_be_deleted = User.query.filter_by(username=username).first()
    ts_of_that_user = Timesheet.query.filter_by(user_id=user_to_be_deleted.id).all()

    if not user_to_be_deleted:
        return jsonify({'message':'user does not exist'})

    if len(ts_of_that_user) > 0:
        db.session.delete(ts_of_that_user)

    db.session.delete(user_to_be_deleted)
    db.session.commit()
    return user_schema.jsonify(user_to_be_deleted)

# @app.route('/api/v1/timesheet/<int:id>', methods=['DELETE'])
# def delete_timesheet(id):
#     ts = Timesheet.query.filter_by(id = id).first()
#     if not ts:
#         return jsonify({'message':'timesheet does not exist'})
#     db.session.delete(ts)
#     db.session.commit()
#     return timesheet_schema.jsonify(ts)

#
# # patch a user to clock in
# @app.route('/api/v1/user/<int:uid>', methods=['PATCH'])
# def patch_user(uid):
#
#     user = User.query.filter_by(id=uid).first()
#
#     if user is not None and user.is_approved and not user.is_admin:
#         todays_date = datetime.now().date()
#         wanted_row = Timesheet.query.filter_by(and_(user_id = user.id, todays_date = todays_date)).first()
#
#         if todays_date == wanted_row.todays_date:
#             if wanted_row.is_clocked_in:
#                 return user_schema.jsonify(user)
#             else:
#                 wanted_row.is_clocked_in = True
#                 wanted_row.todays_date = datetime.now().date()
#                 wanted_row.clock_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 db.session.commit()
#                 return user_schema.jsonify(user)
#         else:
#             # that means that the user is on a new day to work
#             # now we will create a new timesheet row which will let to clock in and stamp its time
#             # then we will add it to the db session
#             new_time_row = Timesheet(is_clocked_in=True, todays_date = datetime.now().date(), clock_in_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id = user.id)
#             db.session.add(new_time_row)
#             db.session.commit()
#             return user_schema.jsonify(user)
#
#
#     return jsonify({'message':'some_other_errors'})
#
#
# """
#     --> Custom GET method that returns JSON
# """
# # patch a user to clock out
# @app.route('/api/v1/func/clock/<string:username>', methods=['GET'])
# def clock_user(username):
#
#     """
#         This function must be only used within that dashboard for approved users, since no error checks are handled.
#     """
#     user = User.query.filter_by(username=username).first()
#
#     if user is not None:
#         todays_date = datetime.now().date()
#         wanted_row = Timesheet.query.filter_by(and_(user_id = user.id, todays_date = todays_date)).first()
#
#         print(f"Shows what wanted_row returns {str(wanted_row)}")
#
#         if todays_date == wanted_row.todays_date:
#             if wanted_row.is_clocked_in:
#                 wanted_row.is_clocked_in = False
#                 wanted_row.clock_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 db.session.commit()
#                 return user_schema.jsonify(user)
#             else:
#                 return jsonify({'message':'it is already clocked out'})
#
#
#     return jsonify({'message':'some_other_errors'})
#
#
#
#
#
#
#
"""
    EMAIL Routes & Other Configs
"""
@app.route("/confirm/<string:id>/<string:token>")
def confirm(id, token):
    current_user = User.query.get(id)
    if current_user.confirmed:
        flash("Your account is already activated")
    elif current_user.confirm(token):
        flash("Your account is now confirmed")
        current_user.confirmed = True
        db.session.commit()
    else:
        flash("Your confirmation link is invalid or has expired")
    return redirect(url_for("home"))

@app.route("/reset/<string:id>/<string:token>", methods=['GET', 'POST'])
def reset(id, token):
    form = PasswordResetForm()
    user = User.query.get(id)
    if user.confirmresettoken(token):
        if (form.validate_on_submit()):
            hashed_password = hash_password(password = form.new_password.data)
            if(check_password(form.new_password.data, user.password)):
                flash("Cannot reset password to your current password")
            else:
                flash("Password reset!")
                user.password = hashed_password
                db.session.commit()
                return redirect(url_for("home"))
    else:
        flash("Your token is invalid and/or expired")
        return redirect(url_for("home"))
    return render_template('reset.html', form=form, title= "Password Reset")



# resetmessage asks for a valid email, then it sends a password reset email to the user
@app.route("/resetmessage", methods=['GET','POST'])
def resetmessage():
    form = EmailPasswordForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("email sent")
            send_email2(form.email.data, "password reset email", render_template('resetmessage.html', current_user=user, token=user.generate_reset_token()))
            return redirect(url_for("home"))
        else:
            flash("invalid email address")
    return render_template('emailpasswordreset.html', form=form, title="Password Reset")
