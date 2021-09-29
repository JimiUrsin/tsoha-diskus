from app import db
import counter

def forum(forum_id):
    sql = "DELETE FROM forums WHERE forums.id=:id"
    db.session.execute(sql, {"id":forum_id})
    db.session.commit()

def thread(forum_id, thread_id, admin, user_id):
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

    counter.sub(forum_id, count)    

def message(message_id, admin, user_id, thread_id):
    if admin:
        sql = "DELETE FROM messages WHERE id=:message_id"
        params = {"message_id":message_id}
    else:
        sql = "DELETE FROM messages WHERE id=:message_id AND user_id=:user_id;"
        params = {"message_id":message_id, "user_id":user_id}

    db.session.execute(sql, params)
    db.session.commit()

    counter.decrement(thread_id)