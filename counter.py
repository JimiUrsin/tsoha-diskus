from app import db
from get import parent

def increment(thread_id):    
    sql = "UPDATE threads SET msgcount=msgcount+1 WHERE id=:thread_id;"       
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

    parent_id = parent(thread_id)
    sql = "UPDATE forums SET msgcount=msgcount+1 WHERE id=:forum_id;"    
    db.session.execute(sql, {"forum_id":parent_id})
    db.session.commit()

def decrement(thread_id):
    sql = "UPDATE threads SET msgcount=msgcount-1 WHERE id=:thread_id;"       
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

    parent_id = parent(thread_id)
    sql = "UPDATE forums SET msgcount=msgcount-1 WHERE id=:forum_id;"    
    db.session.execute(sql, {"forum_id":parent_id})
    db.session.commit()

def sub(forum_id, amount):
    sql = f"UPDATE forums SET msgcount=msgcount-{amount} WHERE id=:forum_id;"    
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()

def increment_tc(forum_id):
    sql = "UPDATE forums SET threadcount=threadcount+1 WHERE id=:forum_id;" 
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()

def decrement_tc(forum_id):
    sql = "UPDATE forums SET threadcount=threadcount-1 WHERE id=:forum_id;" 
    db.session.execute(sql, {"forum_id":forum_id})
    db.session.commit()