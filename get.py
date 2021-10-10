from app import db
from datetime import datetime

def forum_exists(forum_id):
    sql = "SELECT 1 FROM forums WHERE id=:forum_id;"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone() is not None

def get_forums():
    subquery = "SELECT forums.id, MAX(messages.sent_at) AS lastmsg FROM messages " \
    "LEFT JOIN threads ON messages.thread_id=threads.id " \
    "LEFT JOIN forums ON threads.forum_id=forums.id " \
    "GROUP BY forums.id"

    sql = "SELECT forums.*, subq.lastmsg FROM forums " \
    f"LEFT JOIN ({subquery}) AS subq ON subq.id=forums.id"
    result = db.session.execute(sql)
    forums = result.fetchall()
    return forums

def get_threads(forum_id):
    subquery = "SELECT threads.id, MAX(messages.sent_at) AS lastmsg FROM messages " \
    "LEFT JOIN threads ON messages.thread_id=threads.id " \
    "LEFT JOIN forums ON threads.forum_id=forums.id " \
    "GROUP BY threads.id"

    sql = "SELECT threads.id, threads.title, threads.msgcount, users.username, subq.lastmsg FROM threads " \
        "LEFT JOIN users ON threads.created_by=users.id " \
        f"LEFT JOIN ({subquery}) AS subq ON subq.id=threads.id" \
        " WHERE threads.forum_id=:id"
    result = db.session.execute(sql, {"id":forum_id})
    return result.fetchall()

def messages(thread_id):
    sql = "SELECT messages.*, users.username FROM messages " \
    "LEFT JOIN users ON messages.user_id=users.id WHERE thread_id=:id;"
    result = db.session.execute(sql, {"id":thread_id})
    return result.fetchall()

def forum(forum_id):
    sql = "SELECT * FROM forums WHERE id=:id;"
    result = db.session.execute(sql, {"id":forum_id})
    return result.fetchone()

def thread(thread_id):
    sql = "SELECT * FROM threads WHERE id=:id;"    
    result = db.session.execute(sql, {"id": thread_id})
    return result.fetchone()

def parent(thread_id):
    sql = "SELECT forum_id FROM threads WHERE id=:thread_id;"
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchone()[0]

def search(query):
    sql = "SELECT messages.*, threads.title FROM messages " \
    "LEFT JOIN threads ON threads.id=messages.thread_id " \
    "WHERE messages.content LIKE :query;"
    result = db.session.execute(sql, {"query":f"%{query}%"})
    return result.fetchall()

