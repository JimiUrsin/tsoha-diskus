from flask import render_template, redirect, request, session, flash
from app import app

import create
import get
import user
import delete

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
        if forum[1] and not session["admin"]:
            return redirect("/")
        return render_template("forum.html", forum=forum, threads=threads)
    else:
        return redirect("/")


@app.route("/createthread", methods=["POST"])
def createthread():
    if session["id"]:
        title = request.form["title"]
        forum_id = request.form["forum_id"]

        if len(title) > 50:
            return error("Langan otsikko ei saa olla yli 50 merkkiä pitkä", "/")

        if not create.create_thread(title, forum_id, session["id"]):
            flash("Langan otsikko ei voi olla tyhjä.") 

    return redirect(f"/forums/{forum_id}")

@app.route("/deletethread", methods=["POST"])
def deletethread():
    thread_id = request.form["thread_id"]
    forum_id = request.form["forum_id"]

    delete.thread(forum_id, thread_id, session["admin"], session["id"])

    return redirect(f"/forums/{forum_id}")


@app.route("/createforum", methods=["POST"])
def createforum():
    if session["admin"]:
        topic = request.form["topic"]
        hidden = request.form.get("hidden")
        
        if len(topic) > 500:
            return error("Aihe ei saa olla yli 50 merkkiä pitkä", "/")

        if not create.create_forum(topic, bool(hidden)):
            flash("Aiheen nimi ei voi olla tyhjä.")       

    return redirect("/")

@app.route("/deleteforum", methods=["POST"])
def deleteforum():
    if session["admin"]:
        forum_id = request.form["forum_id"]
        delete.forum(forum_id)
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]

    if password != confirm:
        return error("Salasanat eivät täsmää", request.path)
    if len(username) > 64:
        return error("Käyttäjätunnus on liian pitkä", request.path)
    if len(password) > 64:        
        return error("Salasana on liian pitkä", request.path)
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

    username = request.form["username"]
    if not user.user_exists(username):
        flash("Väärä käyttäjänimi")
        return redirect("/login")
    
    password = request.form["password"]
    account = user.check_password(username, password)
    if account is None:
        flash("Väärä salasana")
        return redirect("/login")
    else:
        session["id"] = account[0]
        session["admin"] = account[1]
        session["username"] = account[2]
    return redirect("/")
    

@app.route("/logout")
def logout():
    del session["username"]
    del session["admin"]
    del session["id"]
    return redirect("/")

@app.route("/promote/")
def promote():
    if session["id"]:
        user.promote(session["id"])
        session["admin"] = True
    return redirect("/")

@app.route("/demote/")
def demote():
    if session["id"]:
        user.demote(session["id"])
        session["admin"] = False
    return redirect("/")

@app.route("/thread/<int:id>")
def thread(id):
    thread = get.thread(id)
    
    if thread is None:
        return redirect("/")
    
    parent_id = get.parent(id)
    forum = get.forum(parent_id)
    if forum[1] and not session["admin"]:              
        return redirect("/")

    messages = get.messages(id)
    return render_template("thread.html", messages=messages, thread=thread)

@app.route("/createmessage", methods=["POST"])
def createmessage():
    if not session["username"]:
        return redirect("/")
    text = request.form["content"]
    thread_id = request.form["thread_id"]    
    if len(text) > 500:
        return error("Viesti ei saa olla yli 500 merkkiä pitkä", f"/thread/{thread_id}")
    if not create.create_message(text, thread_id, session["id"]):        
        flash("Viesti ei voi olla tyhjä.")
    return redirect(f"/thread/{thread_id}")

@app.route("/deletemessage", methods=["POST"])
def deletemessage():
    message_id = request.form["message_id"]
    thread_id = request.form["thread_id"]

    delete.message(message_id, session["admin"], session["id"], thread_id)

    return redirect(f"/thread/{thread_id}")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html", searched=False)
    
    
    query = request.form["query"]
    if not query.strip():
        return error("Hakusana ei saa olla tyhjä", "/search")
    messages = get.search(query)
    return render_template("search.html", messages=messages, searched=True, query=query)

def error(message, destination):
    flash(message)
    return redirect(destination)