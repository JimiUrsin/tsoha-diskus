from flask import render_template, redirect, request, session, flash
from app import app

import create
import get
import user
import delete
from thread import edit_thread, create_thread

@app.route("/")
def index():
    forums = get.get_forums()
    return render_template("index.html", forums = forums)

@app.route("/forums/<int:id>")
def forum(id):
    exists = get.forum_exists(id)

    if exists:
        threads = get.get_threads(id)
        forum = get.forum(id)
        if forum[1] and not session.get("admin"):
            return redirect("/")
        return render_template("forum.html", forum=forum, threads=threads)
    else:
        return redirect("/")


@app.route("/createthread", methods=["POST"])
def createthread():
    if session.get("id"):
        title = request.form.get("title")
        forum_id = request.form.get("forum_id")

        if len(title) > 50:
            return error("Langan otsikko ei saa olla yli 50 merkkiä pitkä", f"/forums/{forum_id}")

        if not create_thread(title, forum_id, session["id"]):
            flash("Langan otsikko ei voi olla tyhjä.") 

    return redirect(f"/forums/{forum_id}")

@app.route("/deletethread", methods=["POST"])
def deletethread():
    thread_id = request.form.get("thread_id")
    forum_id = request.form.get("forum_id")

    if thread_id:
        delete.thread(forum_id, thread_id, session.get("admin"), session.get("id"))

    return redirect(f"/forums/{forum_id}")


@app.route("/createforum", methods=["POST"])
def createforum():
    if session.get("admin"):
        topic = request.form.get("topic")
        hidden = request.form.get("hidden")
        
        if len(topic) > 50:
            return error("Aihe ei saa olla yli 50 merkkiä pitkä", "/")

        if not create.create_forum(topic, bool(hidden)):
            flash("Aiheen nimi ei voi olla tyhjä.")       

    return redirect("/")

@app.route("/deleteforum", methods=["POST"])
def deleteforum():
    if session.get("admin"):
        forum_id = request.form.get("forum_id")
        delete.forum(forum_id)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    confirm = request.form.get("confirm", "").strip()

    if not username or not 3 <= len(username) <= 64:
        return error("Käyttäjätunnuksen tulee olla 3–64 merkkiä pitkä.", request.path)
    if not password or not 4 <= len(password) <= 64:
        return error("Salasanan tulee olla 4–64 merkkiä pitkä.", request.path)
    if password != confirm:
        return error("Salasanat eivät täsmää", request.path)
    if user.user_exists(username):
        return error("Käyttäjätunnus on jo olemassa", request.path)

    user.register(username, password)

    account = user.get_user(username)

    session["username"] = username
    session["admin"] = False
    session["id"] = account[0]
    return redirect("/")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "")
    if not username.strip() or not user.user_exists(username):
        return error("Väärä käyttäjänimi", request.path)
    
    password = request.form.get("password", "")
    if not password.strip():
        return error("Väärä salasana", request.path)

    account = user.check_password(username, password)

    if account is None:
        return error("Väärä salasana", request.path)
    else:
        session["id"] = account[0]
        session["admin"] = account[1]
        session["username"] = account[2]
    return redirect("/")
    

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("admin", None)
    session.pop("id", None)
    return redirect("/")

@app.route("/promote/")
def promote():
    user_id = session.get("id")
    if user_id:
        user.promote(user_id)
        session["admin"] = True
    return redirect("/")

@app.route("/demote/")
def demote():
    user_id = session.get("id")
    if user_id:
        user.demote(user_id)
        session["admin"] = False
    return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    thread = get.thread(id)
    
    if thread is None:
        return redirect("/")
    
    parent_id = get.parent(id)
    forum = get.forum(parent_id)
    if forum[1] and not session.get("admin"):
        return redirect("/")

    messages = get.messages(id)
    return render_template("thread.html", messages=messages, thread=thread)

@app.route("/createmessage", methods=["POST"])
def createmessage():
    if not session.get("username"):
        return redirect("/")

    text = request.form.get("content")
    thread_id = request.form.get("thread_id", "-1")
    if len(text) > 500:
        return error("Viesti ei saa olla yli 500 merkkiä pitkä", f"/thread/{thread_id}")
    if not create.create_message(text, thread_id, session.get("id")):        
        flash("Viesti ei voi olla tyhjä.")
    return redirect(f"/thread/{thread_id}")

@app.route("/deletemessage", methods=["POST"])
def deletemessage():
    message_id = request.form.get("message_id")
    thread_id = request.form.get("thread_id", "0")

    if message_id:
        delete.message(message_id, session.get("admin"), session.get("id"), thread_id)

    return redirect(f"/thread/{thread_id}")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html", searched=False)
    
    
    query = request.form.get("query", "")
    if not query.strip():
        return error("Hakusana ei saa olla tyhjä", "/search")
    messages = get.search(query)
    return render_template("search.html", messages=messages, searched=True, query=query)

@app.route("/editthread", methods=["POST"])
def editthread():
    thread_id=request.form.get("thread_id")
    title=request.form.get("title", "")
    forum_id=request.form.get("forum_id")

    if not title.strip():
        return error("Aihe ei saa olla tyhjä", f"/forums/{forum_id}")

    if thread_id and title:
        if len(title) > 50:
            return error("Aihe ei saa olla yli 50 merkkiä pitkä", f"/forums/{forum_id}")
        edit_thread(thread_id, title, session.get("admin", False), session.get("id", 0))
    
    return redirect(f"/forums/{forum_id}")

@app.route("/editmessage", methods=["POST"])
def editmessage():
    return redirect("/")

def error(message, destination):
    flash(message)
    return redirect(destination)