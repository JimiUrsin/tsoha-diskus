from app import db
from counter import increment

def create_forum(topic, hidden):
    if topic.strip():
        sql = "INSERT INTO forums (hide, topic) VALUES (:hide, :topic);"
        db.session.execute(sql, {"hide":hidden, "topic":topic})
        db.session.commit()
        return True
    return False

def create_message(text, thread_id, user_id):
    if text.strip():
        sql = "INSERT INTO messages (thread_id, user_id, content, sent_at) VALUES (:thread_id, :user_id, :content, NOW());"
        db.session.execute(sql, {"thread_id":thread_id, "user_id":user_id, "content":text})
        db.session.commit()

        increment(thread_id)

        return True
    return False