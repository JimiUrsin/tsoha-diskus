from app import db
from counter import decrement, increment

def create(text, thread_id, user_id):
    if text.strip():
        sql = "INSERT INTO messages (thread_id, user_id, content, sent_at) VALUES (:thread_id, :user_id, :content, NOW());"
        db.session.execute(sql, {"thread_id":thread_id, "user_id":user_id, "content":text})
        db.session.commit()

        increment(thread_id)

        return True
    return False

def delete(message_id, admin, user_id, thread_id):
    if admin:
        sql = "DELETE FROM messages WHERE id=:message_id"
        params = {"message_id":message_id}
    else:
        sql = "DELETE FROM messages WHERE id=:message_id AND user_id=:user_id;"
        params = {"message_id":message_id, "user_id":user_id}

    db.session.execute(sql, params)
    db.session.commit()

    decrement(thread_id)

def edit(message_id, content, admin, user_id):
    if admin:
        sql = "UPDATE messages SET content=:content WHERE id=:message_id;"
    else:
        sql = "UPDATE messages SET content=:content WHERE id=:message_id AND user_id=:user_id;"
    
    db.session.execute(sql, {"content":content, "message_id":message_id, "user_id":user_id})
    db.session.commit()