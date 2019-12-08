from base64 import b64encode, b64decode
from hashlib import sha512
from passlib.hash import argon2
from sqlite3 import connect
from smartclock import database_name
from datetime import datetime
from os import path


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
    Utilities
"""

def getDuration(then, now = datetime.now(), interval = "default"):

    """
    Written by Stack Overflow user, Attaque.
    https://stackoverflow.com/users/1116508/attaque

    """
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = now - then # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def days(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 86400) # Seconds in a day = 86400

    def hours(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minutes(seconds = None):
      return divmod(seconds if seconds != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconds(seconds = None):
      if seconds != None:
        return divmod(seconds, 1)
      return duration_in_s

    def totalDuration():
        y = years()
        d = days(y[1]) # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'years': int(years()[0]),
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': totalDuration()
    }[interval]
