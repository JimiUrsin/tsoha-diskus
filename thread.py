from app import db
from counter import increment_tc

def edit_thread(thread_id, title, admin, user_id):
    if admin:
        sql = "UPDATE threads SET title=:title WHERE threads.id=:thread_id"
    else:
        sql = "UPDATE threads SET title=:title WHERE threads.id=:thread_id AND threads.created_by=:user_id;"
    
    db.session.execute(sql, {"title":title, "thread_id":thread_id, "user_id":user_id})
    db.session.commit()

def create_thread(title, forum_id, user_id):
    if title.strip():
        sql = "INSERT INTO threads(forum_id, created_by, title, created_at) VALUES (:forum_id, :user_id, :title, NOW())"
        db.session.execute(sql, {"forum_id":forum_id, "user_id":user_id, "title":title})
        db.session.commit()
        increment_tc(forum_id)
        return True
    return False