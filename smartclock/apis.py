from smartclock import app, db
from flask import request, jsonify
from smartclock.models import User, Timesheet, user_schema, users_schema, timesheet_schema, timesheets_schema
from smartclock.functions import hash_password
from datetime import datetime

# REST API Implementation

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
    confirmed = request.json['confirmed']
    timesheets = request.json['timesheets']

    if username and password and hashed_password and first_name and last_name and email and is_approved and is_admin \
        and confirmed and timesheets:
        new_user = User(username=username, timesheets=timesheets, first_name=first_name, last_name=last_name, email=email,
                        is_admin=is_admin, is_approved=is_approved, password=hashed_password, confirmed=confirmed)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)
    else:
        return jsonify("custom_message_error", "one of the fields in the list are missing from username and password"+
                       "and hashed_password and first_name and last_name and email and is_approved and is_admin "+
                       "and confirmed and timesheets")

# with this command update any field of a user except id and password
@app.route('/api/v1/user/patch/<username>', methods=['PATCH'])
def patch_anything(username):
    user = User.query.filter_by(username=username).first()
    if user:
        for key in request.json:
            if key == 'is_admin':
                user.is_admin = request.json[key]
            elif key == 'is_approved':
                user.is_approved = request.json[key]
            elif key == 'confirmed':
                user.confirmed = request.json[key]
            elif key == 'username':
                user.username = request.json[key]
            elif key == 'first_name':
                user.first_name = request.json[key]
            elif key == 'last_name':
                user.last_name = request.json[key]
            elif key == 'email':
                user.email = request.json[key]
            elif key == 'timesheets':
                user.timesheets = request.json[key]
        db.session.commit()
        return user_schema.jsonify(user)
    else:
        return jsonify("custom_message_error", "user doesn't exist with that given username")

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

# delete a user by id
@app.route('/api/v1/user/<username>', methods=['DELETE'])
def delete_user(username):

    user_to_be_deleted = User.query.filter_by(username=username).first()
    ts_of_that_user = Timesheet.query.filter_by(user_id=user_to_be_deleted.id).all()

    if not user_to_be_deleted:
        return jsonify({'message':'user does not exist'})

    if len(ts_of_that_user) > 0:
        db.session.delete(ts_of_that_user)

    db.session.delete(user_to_be_deleted)
    db.session.commit()
    return user_schema.jsonify(user_to_be_deleted)

# delete a timesheet by id
@app.route('/api/v1/timesheet/<int:id>', methods=['DELETE'])
def delete_timesheet(id):
    ts = Timesheet.query.filter_by(id = id).first()
    if not ts:
        return jsonify({'message':'timesheet does not exist'})
    db.session.delete(ts)
    db.session.commit()
    return timesheet_schema.jsonify(ts)

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