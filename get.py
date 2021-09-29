from app import db

def forum_exists(forum_id):
    sql = "SELECT 1 FROM forums WHERE id=:forum_id;"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone() is not None

def get_forums():
    sql = f"SELECT forums.* FROM forums;"
    result = db.session.execute(sql)
    forums = result.fetchall()
    return forums

def get_threads(forum_id):
    sql = "SELECT threads.id, threads.title, threads.msgcount, users.username FROM threads " \
        "LEFT JOIN users ON threads.created_by=users.id WHERE threads.forum_id=:id;"    
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

def thread_count(forum_id):
    sql = "SELECT COUNT(id) FROM threads WHERE forum_id=:forum_id;"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone()[0]

def forum_message_count(forum_id):
    sql = "SELECT COUNT(messages.id) FROM messages " \
    "LEFT JOIN threads ON messages.thread_id=threads.id " \
    "LEFT JOIN forums ON threads.forum_id=forums.id " \
    "WHERE messages.thread_id=threads.id AND threads.forum_id=:forum_id"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone()[0]

def thread_message_count(thread_id):
    sql = "SELECT COUNT(id) FROM messages WHERE thread_id=:thread_id"    
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchone()[0]

def parent(thread_id):
    sql = "SELECT forum_id FROM threads WHERE id=:thread_id;"
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchone()[0]