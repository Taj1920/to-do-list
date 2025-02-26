import sqlite3
def init_db():
    conn=sqlite3.connect('data.db',check_same_thread=False)
    c=conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS USER(id integer primary key autoincrement,uname varchar,pwd varchar)')
    c.execute('CREATE TABLE IF NOT EXISTS TASKS(ID INTEGER PRIMARY KEY AUTOINCREMENT,TITLE VARCHAR,COMPLETED BOOLEAN,USER INTEGER NOT NULL,FOREIGN KEY (USER)  REFERENCES USER(ID))')
    conn.commit()
    conn.close()
