from werkzeug.security import check_password_hash, generate_password_hash
from app import db

def user_exists(username):    
    sql = "SELECT users.id FROM users WHERE username=:name"
    result = db.session.execute(sql, {"name":username}).fetchone()
    return result is not None

def get_user(username):
    sql = "SELECT * FROM users WHERE username=:name"    
    return db.session.execute(sql, {"name":username}).fetchone()

def register(username, password):
    pwhash = generate_password_hash(password)
    sql = "INSERT INTO users (administrator, username, pwhash) VALUES ('false', :name, :pw);"
    db.session.execute(sql, {"name":username, "pw":pwhash})
    db.session.commit()

def check_password(username, password):
    user_sql = "SELECT pwhash FROM users WHERE username=:username"
    pwhash = db.session.execute(user_sql, {"username":username}).fetchone()[0]
    if check_password_hash(pwhash, password):
        return get_user(username)
    else:
        return None

def promote(user_id):
    sql = "UPDATE users SET administrator='1' WHERE id=:id;"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def demote(user_id):
    sql = "UPDATE users SET administrator='0' WHERE id=:id;"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()