import sqlite3
from create import *
conn=sqlite3.connect('data.db',check_same_thread=False)
c=conn.cursor()



def get_task(user):
    c.execute(f'SELECT ID,TITLE,COMPLETED,DUE_DATE FROM TASKS WHERE USER="{user}"')
    return c.fetchall()

def add_task(user_id,task,due_date):
    init_db()
    c.execute('INSERT INTO TASKS (USER,TITLE,DUE_DATE,COMPLETED) VALUES(?,?,?,?)',(user_id,task,due_date,False))
    conn.commit()

def complete_task(task_id):
    c.execute(f'UPDATE TASKS SET COMPLETED={True} WHERE ID={task_id}')
    conn.commit()
def pending_task(task_id):
    c.execute(f'UPDATE TASKS SET COMPLETED={False} WHERE ID={task_id}')
    conn.commit()

def reset_auto_increment():
    c.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'TASKS'")
    conn.commit()


def delete_task(task_id):
    c.execute(f'DELETE FROM TASKS WHERE ID={task_id}')
    conn.commit()
    reset_auto_increment()
    