from app import db

def edit_message(message_id, content, admin, user_id):
    if admin:
        sql = "UPDATE messages SET content=:content WHERE id=:message_id;"
    else:
        sql = "UPDATE messages SET content=:content WHERE id=:message_id AND user_id=:user_id;"
    
    db.session.execute(sql, {"content":content, "message_id":message_id, "user_id":user_id})
    db.session.commit()