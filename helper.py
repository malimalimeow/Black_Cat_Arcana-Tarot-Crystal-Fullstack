from functools import wraps
from flask import request, redirect, session, flash
import re
from cs50 import SQL
from datetime import datetime, timedelta


db=SQL("sqlite:///crystal.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def time_check():
    roll=True
    row=db.execute("SELECT * FROM records WHERE user_id=? AND TIME IS NOT NULL ORDER BY TIME DESC",session["user_id"])
    if row:

        time_last=datetime.strptime(row[0]["time"], "%Y-%m-%d %H:%M:%S")

        time_now=datetime.now()

        different=time_now - time_last


        if different < timedelta(hours=24)  :
            roll=False
            remaining_time=timedelta(hours=24)-different
            remaining_time=int(remaining_time.total_seconds())
            return roll, remaining_time

        else:
            roll=True
            remaining_time=None
            return roll, remaining_time

    else:
        remaining_time=None
        return roll, remaining_time



def get_crystal():
    return db.execute("SELECT * FROM crystals")

def username_validation_checker(u):
    match_username = re.match(r"^[a-zA-Z0-9._]{8,}$",u)
    if not match_username:
        flash("invalid username")
        return False
    return True


def password_validation_checker(p):
    match_password = re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[._!$^@*%&#+-])[a-zA-Z0-9._!$^@%*&#+-]{8,16}$",p)
    if not match_password:
        flash("invalid password")
        return False
    return True