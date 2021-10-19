from app import db
from counter import decrement_tc, increment_tc, sub

def create(title, forum_id, user_id):
    if title.strip():
        sql = "INSERT INTO threads(forum_id, created_by, title, created_at) VALUES (:forum_id, :user_id, :title, NOW())"
        db.session.execute(sql, {"forum_id":forum_id, "user_id":user_id, "title":title})
        db.session.commit()
        increment_tc(forum_id)
        return True
    return False

def delete(forum_id, thread_id, admin, user_id):
    count_sql = "SELECT msgcount FROM threads WHERE threads.id=:thread_id;"
    count = db.session.execute(count_sql, {"thread_id":thread_id}).fetchone()[0]

    if admin:
        sql = "DELETE FROM threads WHERE id=:thread_id"
        params = {"thread_id":thread_id}
    else:
        sql = "DELETE FROM threads WHERE id=:thread_id AND created_by=:user_id;"
        params = {"thread_id":thread_id, "user_id":user_id}    

    db.session.execute(sql, params)
    db.session.commit()

    sub(forum_id, count)
    decrement_tc(forum_id)

def edit(thread_id, title, admin, user_id):
    if admin:
        sql = "UPDATE threads SET title=:title WHERE threads.id=:thread_id;"
    else:
        sql = "UPDATE threads SET title=:title WHERE threads.id=:thread_id AND threads.created_by=:user_id;"
    
    db.session.execute(sql, {"title":title, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()