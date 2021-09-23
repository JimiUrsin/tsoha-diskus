from os import getenv
from flask import Flask
from flask import render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT * FROM forums;"
    result = db.session.execute(sql)
    forums = result.fetchall()
    return render_template("index.html", forums = forums)

@app.route("/forums/<int:id>")
def forum(id):
    sql = "SELECT * FROM forums WHERE id=:id;"
    result = db.session.execute(sql, {"id":id})
    forum = result.fetchone()
    if forum is None:
        return redirect("/")
    else:
        sql = "SELECT threads.id, threads.title, users.username FROM threads " \
        "LEFT JOIN users ON threads.created_by=users.id WHERE threads.forum_id=:id;"
        result = db.session.execute(sql, {"id":id})
        threads = result.fetchall()
        return render_template("forum.html", forum=forum, threads=threads)


@app.route("/createthread", methods=["POST"])
def createthread():
    title = request.form["title"]
    forum_id = request.form["forum_id"]
    if title is not None:
        sql = "INSERT INTO threads(forum_id, created_by, title, created_at) VALUES (:id, :user, :title, NOW())"
        db.session.execute(sql, {"id":forum_id, "user":session["id"], "title":title})
        db.session.commit()
    return redirect(f"/forums/{forum_id}")

@app.route("/deletethread", methods=["POST"])
def deletethread():
    thread_id = request.form["thread_id"]
    forum_id = request.form["forum_id"]

    sql = "DELETE FROM threads WHERE threads.id=:id"
    db.session.execute(sql, {"id":thread_id})
    db.session.commit()
    return redirect(f"/forums/{forum_id}")


@app.route("/createforum", methods=["POST"])
def createforum():
    topic = request.form["topic"]
    if topic is not None:
        sql = "INSERT INTO forums (hide, topic) VALUES ('FALSE', :topic);"
        db.session.execute(sql, {"topic":topic})
        db.session.commit()
    return redirect("/")

@app.route("/deleteforum", methods=["POST"])
def deleteforum():
    forum_id = request.form["forum_id"]
    sql = "DELETE FROM forums WHERE forums.id=:id"
    db.session.execute(sql, {"id":forum_id})
    db.session.commit()
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def registerp():
    username = request.form["username"]
    sql = "SELECT users.id FROM users WHERE users.username=:name"
    result = db.session.execute(sql, {"name":username})
    if result.fetchone() is None:
        password = request.form["password"]
        sql = "INSERT INTO users (administrator, username, pwhash) VALUES ('false', :name, :pw);"
        db.session.execute(sql, {"name":username, "pw":generate_password_hash(password)})
        db.session.commit()
        sql = "SELECT id FROM users WHERE username=:username;"
        user = db.session.execute(sql, {"username":username}).fetchone()
        session["username"] = username
        session["admin"] = False
        session["id"] = user[0]
    else:
        flash("Käyttäjätunnus on jo olemassa")
        return redirect("/register")
    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginp():
    username = request.form["username"]
    sql = "SELECT id, administrator, pwhash FROM users WHERE users.username=:name"
    result = db.session.execute(sql, {"name":username})
    user = result.fetchone()
    if user is None:
        flash("Väärä käyttäjänimi")
        return redirect("/login")
    else:
        flash("Väärä salasana")
        password = request.form["password"]
        if check_password_hash(user[2], password):
            session["username"] = username
            session["admin"] = user[1]
            session["id"] = user[0]
        else:
            return redirect("/login")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["admin"]
    del session["id"]
    return redirect("/")
        