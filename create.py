import sqlite3
conn=sqlite3.connect('data.db',check_same_thread=False)
c=conn.cursor()

# c.execute('CREATE TABLE USER(id integer primary key autoincrement,uname varchar,pwd varchar)')
# c.execute('CREATE TABLE TASKS(ID INTEGER PRIMARY KEY AUTOINCREMENT,TITLE VARCHAR,COMPLETED BOOLEAN,USER INTEGER NOT NULL,FOREIGN KEY (USER)  REFERENCES USER(ID))')

