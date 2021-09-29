from app import db

def forum_exists(forum_id):
    sql = "SELECT 1 FROM forums WHERE id=:forum_id;"
    result = db.session.execute(sql, {"forum_id":forum_id})
    return result.fetchone() is not None

def get_forums():
    sql = "SELECT * FROM forums;"
    result = db.session.execute(sql)
    forums = result.fetchall()
    return forums

def get_threads(forum_id):
    sql = "SELECT threads.id, threads.title, users.username FROM threads " \
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