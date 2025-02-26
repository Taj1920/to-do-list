import sqlite3
import pickle
from create import *
conn=sqlite3.connect('data.db',check_same_thread=False)
c=conn.cursor()
# c.execute('CREATE TABLE USER(id integer primary key autoincrement,uname varchar,pwd varchar)')
# conn.commit()
def check_user(uname):
    if list(c.execute(f'SELECT * from user')):
        try:
            c.execute(f'SELECT * FROM USER WHERE UNAME = "{uname}"')
            return True
        except:
            return False 
    return True

def get_id():
    if list(c.execute(f'SELECT * from user')):
        return list(c.execute(f'Select max(id) from user'))[0][0] + 1
    return 1

def signup(uname,pwd):
    init_db()
    if check_user(uname):
        user_id = get_id()
        c.execute('INSERT INTO USER(id,uname,pwd) VALUES(?,?,?)',(user_id,uname,pwd))
        conn.commit()
        return True
    else:
        return False

def login(uname,pwd):
    l=list(c.execute('SELECT UNAME,PWD FROM USER'))
    if (uname,pwd) in l:
        return list(c.execute(f'SELECT ID FROM USER where uname="{uname}"'))[0][0]
    else:
        return ()
