from app import db

def create(topic, hidden):
    if topic.strip():
        sql = "INSERT INTO forums (hide, topic) VALUES (:hide, :topic);"
        db.session.execute(sql, {"hide":hidden, "topic":topic})
        db.session.commit()
        return True
    return False

def delete(forum_id):
    if (forum_id):
        sql = "DELETE FROM forums WHERE forums.id=:id"
        db.session.execute(sql, {"id":forum_id})
        db.session.commit()