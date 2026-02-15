from datetime import datetime
import random
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import login_required, time_check, get_crystal, username_validation_checker, password_validation_checker

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///crystal.db")

with open("tarot.json", "r", encoding="utf-8") as json_file:
    tarot_cards = json.load(json_file)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()

        if not request.form.get("username") or not request.form.get("password"):
            flash("must provide username and password")
            return redirect("/login")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("no match record")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]
        date = datetime.today()
        db.execute("INSERT INTO records(user_id ,log_in_date) VALUES (?, DATE(?))",
                   session["user_id"], date)

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username_in = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username_in or not password or not confirmation:
            flash("must provide username and password")
            return redirect("/registration")

        row = db.execute("SELECT * FROM users WHERE username=?", username_in)
        if row:
            flash("user already existed")
            return redirect("/login")

        if username_validation_checker(username_in) == False or password_validation_checker(password) == False:
            flash("invalid username/ password")
            return redirect("/registration")

        hash_password = generate_password_hash(password, method="scrypt", salt_length=16)
        db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username_in, hash_password)
        flash("registration success")
        return redirect("/login")

    return render_template("registration.html")


@app.route("/renewpw", methods=["GET", "POST"])
@login_required
def renewpw():
    if request.method == "POST":
        username_in = request.form.get("username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not (username_in and old_password and new_password and confirmation):
            flash("must provide all the data needed")
            return redirect("/renewpw")

        row = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
        username = row[0]["username"]
        old_hash = row[0]["hash"]

        if username_in != username:
            flash("wrong username")
            return redirect("/renewpw")

        if not check_password_hash(old_hash, old_password):
            flash("wrong old password")
            return redirect("/renewpw")

        if password_validation_checker(new_password) == False:
            flash("invalid new password")
            return redirect("/renewpw")

        if new_password != confirmation:
            flash("password not match")
            return redirect("/renewpw")

        db.execute("UPDATE users SET hash=? WHERE username=?", generate_password_hash(
            new_password, method="scrypt", salt_length=16), username_in)
        flash("user password updated")
        return redirect("/")

    else:
        return render_template("renewpw.html")


@app.route("/tarot", methods=["GET", "POST"])
@login_required
def tarot():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "draw":
            roll, remaining_time = time_check()
            if roll == True:
                return redirect("/lucky")

            elif roll == False:
                flash("only available once within 24 hours")
                return render_template("tarot.html", remaining_time=remaining_time)

        elif action == "record":
            row = db.execute(
                "SELECT card,time FROM records WHERE user_id=? ORDER BY time DESC", session["user_id"])

            last_record_card = row[0]["card"]

            if last_record_card == None:
                flash("No record yet, Draw your first card!")
                return render_template("tarot.html")

            else:
                card_info = tarot_cards[last_record_card]

                return render_template("lucky.html", card=last_record_card, card_info=card_info)

    return render_template("tarot.html", remaining_time=None)


@app.route("/lucky")
@login_required
def lucky():

    time_now = datetime.now()

    cards = list(tarot_cards.keys())

    card = random.choice(cards)

    card_info = tarot_cards[card]

    db.execute("INSERT INTO records (user_id, time, card) VALUES(?, ?, ?)",
               session["user_id"], time_now, card)
    return render_template("lucky.html", card=card, card_info=card_info)


# to take "choice" from lucky.html
@app.route("/choice_record", methods=["POST"])
@login_required
def choice_record():
    if request.method == "POST":
        category = request.form.get("choice")
        c_name = request.form.get("name")
       
        row=db.execute("SELECT time from records WHERE user_id=? AND card IS NOT NULL ORDER BY time DESC LIMIT 1",session["user_id"])
        if row:
            db.execute("UPDATE records SET choice=? WHERE user_id=? AND time=?",category,session["user_id"],row[0]['time'])
            
        return redirect(f"/crystals/{c_name}")


@app.route("/crystals/<crystal_name>", methods=["GET", "POST"])
@login_required
def crystal(crystal_name):
    # show specific crystal info
    crystal_info = get_crystal()

    match = None
    for c in crystal_info:
        if c["name"] == crystal_name:
            match = c
            break

    if not match:
        return redirect("/crystalshowcase")

    name = match["name"]
    crystal_id = match["id"]

    row = db.execute("SELECT * FROM favourite WHERE user_id=? and crystal_id=?",
                     session["user_id"], crystal_id)
    if row:
        favourite = True
    else:
        favourite = False

    # click favourite
    if request.method == "POST":
        status = (request.data.decode()).capitalize()

        if status == "False":
            db.execute("DELETE FROM favourite WHERE user_id=? and crystal_id=?",
                       session["user_id"], crystal_id)

        else:
            db.execute("INSERT INTO favourite(user_id,crystal_id) VALUES (?, ?)",
                       session["user_id"], crystal_id)

        return redirect(f"/crystals/{name}")

    return render_template("crystal.html", crystal=match, favourite=favourite)


@app.route("/favourite")
@login_required
def favourite():

    favourite = db.execute(
        "SELECT * FROM favourite JOIN crystals ON favourite.crystal_id = crystals.id WHERE user_id =? GROUP BY crystals.name", session["user_id"])

    return render_template("favourite.html", favourite=favourite)


@app.route("/crystalshowcase")
def crystal_showcase():
    crystals = get_crystal()

    return render_template("crystalshowcase.html", crystals=crystals)


@app.route("/admin/dashboard1")
@login_required
def dashboard1():
    row = db.execute("SELECT admin FROM users WHERE id=?", session["user_id"])
    if row[0]["admin"] == 0:
        flash("Please login admin account")
        return redirect("/")

    dv_label = []
    dv_value = []
    dt_label = []
    dt_value = []
    top_user = []

    row1 = db.execute("SELECT log_in_date,COUNT(log_in_date) AS view FROM records WHERE log_in_date BETWEEN DATE('now' , '-14 days') AND DATE('now') GROUP BY log_in_date ORDER BY log_in_date DESC")
    for r in row1:
        dv_label.append(r["log_in_date"])
        dv_value.append(r["view"])

    row2 = db.execute(
        "SELECT DATE(time) AS date ,COUNT(card) AS draw FROM records WHERE DATE(time) BETWEEN DATE('now' , '-14 days') AND DATE('now') GROUP BY DATE(time) ORDER BY DATE(time) DESC")
    for r in row2:
        dt_label.append(r["date"])
        dt_value.append(r["draw"])

    row3 = db.execute("SELECT users.username,user_id,COUNT(log_in_date) FROM records JOIN users ON records.user_id= users.id WHERE log_in_date BETWEEN DATE('now' , '-7 days') AND DATE('now') GROUP BY user_id ORDER BY COUNT(log_in_date) DESC LIMIT 5")
    for r in row3:
        top_user.append(r["username"])

    return render_template("dashboard1.html", dv_label=dv_label, dv_value=dv_value, dt_label=dt_label, dt_value=dt_value, top_user=top_user)


@app.route("/admin/dashboard2")
@login_required
def dashboard2():
    row = db.execute("SELECT admin FROM users WHERE id=?", session["user_id"])
    if row[0]["admin"] == 0:
        flash("Please login admin account")
        return redirect("/")

    wtc_label = []
    wtc_value = []
    fr_label = []
    fr_value = []
    c_label = []
    c_value = []

    row1 = db.execute("SELECT crystals.name, favourite.crystal_id, COUNT(*) AS count FROM favourite JOIN crystals ON favourite.crystal_id=crystals.id GROUP BY crystal_id ORDER BY COUNT(*) DESC LIMIT 3;")
    for r in row1:
        wtc_label.append(r["name"])
        wtc_value.append(r["count"])

    row2 = db.execute(
        "SELECT crystals.name,COUNT(DISTINCT user_id) AS like FROM favourite JOIN crystals ON favourite.crystal_id=crystals.id GROUP BY crystals.id")
    row3 = db.execute("SELECT count(*) AS total FROM users")
    total_users = row3[0]['total']
    for r in row2:
        fr_label.append(r["name"])
        fr_value.append((r["like"]/total_users)*100)

    row4 = db.execute(
        "SELECT choice, COUNT(choice) AS count FROM records WHERE choice IS NOT NULL GROUP BY choice")
    row5 = db.execute("SELECT count(choice) AS total FROM records")
    total_choice = row5[0]['total']
    for r in row4:
        c_label.append(r["choice"])
        c_value.append((r["count"]/total_choice)*100)

    return render_template("dashboard2.html", wtc_label=wtc_label, wtc_value=wtc_value, fr_label=fr_label, fr_value=fr_value, c_label=c_label, c_value=c_value)