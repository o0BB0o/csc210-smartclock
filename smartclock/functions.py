from base64 import b64encode, b64decode
from hashlib import sha512
from passlib.hash import argon2
from sqlite3 import connect
from smartclock import database_name
from os import path
from functools import wraps
from flask import abort
from flask_login import current_user
from smartclock.models import Permission


"""
    Password Hashing
    
    A random salt is used inside the argon2.using(rounds=4).hash(sha_hash.digest()) function
    
"""

def hash_password(password):
    sha_hash = sha512(password.encode("utf-8"))
    argon2_hash = argon2.using(rounds=3).hash(sha_hash.digest())
    argon2_hash = argon2_hash.encode() # turns string to 'bytes like object'
    return b64encode(argon2_hash)

def check_password(password, hash_):
    argon2_hash = b64decode(hash_)
    argon2_hash = argon2_hash.decode() # turns 'bytes like object' to string
    sha_hash = sha512(password.encode("utf-8"))
    return argon2.verify(sha_hash.digest(), argon2_hash)


"""
    Database Models
    
    Custom function to handle the table doesn't exist in database
"""

# custom method to handle the database if it doesn't exist
appdir = path.abspath(path.dirname(__file__))
database_location = path.join(appdir, database_name)
#
# def database_exists():
#     return path.exists(database_location)

def tableDoesNotExist(tablename):
    con = connect(database_location)
    c = con.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s' " % tablename)
    if c.fetchone()[0] == 1:
        c.close()
        return False # Table exists
    c.close()
    return True # Table does not exist


"""

    Custom Python Decorators

"""

def permission_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(perm):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
def admin_required(f):
    return permission_required(Permission.ADMIN)(f)