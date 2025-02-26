import streamlit as st
import time
import datetime
import sqlite3
import pandas as pd
import plotly.express as px
from auth import *
from tasks import *
conn=sqlite3.connect('data.db',check_same_thread=False)
c=conn.cursor()

st.set_page_config(page_title='To do list',page_icon='logo.png')
# st.sidebar.title('To-Do List')
st.sidebar.image('logo.png',width=100)
#Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in=False
if 'user' not in st.session_state:
    st.session_state.username=""


if not(st.session_state.logged_in):
    menu=st.sidebar.radio('MENU',['SIGNIN','SIGNUP'])
st.markdown('''
            <h1 style="text-align: center;color:#ffbd33;font-family: Lucida Handwriting">To Do List</h1>

             ''',unsafe_allow_html=True)

if not(st.session_state.logged_in):
    if menu=='SIGNUP':
        if not(st.session_state.logged_in):
            st.write('')
            col1,col2=st.columns([2,1])
            with col1:
                with st.form('signup-form'):
                    uname=st.text_input('Username👤',placeholder='your username..')
                    pwd=st.text_input('Password🔑',placeholder='your password..',type='password')
                    submit=st.form_submit_button('Signup')
                    if submit:
                        if uname and pwd:
                            if signup(uname,pwd):
                                with st.spinner('signing up....'):
                                    time.sleep(2)
                                    st.success('Signup successfull')
                                    st.write('you are ready to login!!')
                            else:
                                st.error('username is already taken')
                        else:
                            st.error('Enter username and password')
                    
            with col2:
                st.title('WELCOME!')
                st.write('Create an Account for free')

    elif menu=='SIGNIN':
            if not(st.session_state.logged_in):
                col1,col2,col3=st.columns([1.5,6,1.5])
                with col2:
                    with st.form('signin-form'):
                        uname=st.text_input('Username👤',placeholder='your username..')
                        pwd=st.text_input('Password🔑',placeholder='your password..',type='password')
                        submit=st.form_submit_button('Signin')
                        if submit:
                            if uname and pwd:
                                user = login(uname,pwd)
                                if user:
                                    with st.spinner('signing in....'):
                                        st.session_state.logged_in=True
                                        st.session_state.user=user
                                        st.session_state.username=uname
                                        time.sleep(2)
                                        st.success('Signin successfull')
                                        st.rerun()
                                else:
                                    st.error('username invalid please signup')
                            else:
                                st.error('Enter username and password')

        

# Task management


if st.session_state.logged_in:
    st.header(f'welcome! {st.session_state.username} 👋')
    st.markdown("#### Manage your tasks efficiently.")
    current_date=datetime.date.today().strftime('%d-%m-%Y')
    if 'tasks' in st.session_state:
        df=pd.DataFrame(st.session_state.tasks,columns=['Id','Task','Completed','Due date'])
        com=df['Completed'][df['Completed']==1].count()
        st.markdown(f"##### Completed Tasks:   {com}/{len(df)}")
        
    #today's Tasks
    with st.container(border=True):
            st.subheader("Today's Tasks 📝")
            st.markdown(f"##### {datetime.date.today().strftime('%d %b')}   ")
            df=pd.DataFrame(get_task(st.session_state.user),columns=['Id','Task','Completed','Due date'])
            df['Due date']=pd.to_datetime(df['Due date']).dt.strftime('%d-%m-%Y')
            today=df[df['Due date']==current_date].iloc[:,1:3]
            today.index=range(1,len(today)+1)
            completed=today['Completed'][today['Completed']==1].count()
            st.markdown(f"###### Completed Tasks:   {completed}/{len(today)}")
            st.dataframe(today,height=200,width=700)
    with st.sidebar:
        with st.container(border=True):
            st.write(f'### {datetime.date.today().strftime('%A')}')
            st.write(current_date)
    
    st.title(' ')

    
    with st.form('add task'):
    #Show task
        if 'tasks' not in st.session_state:
            st.session_state.tasks=get_task(st.session_state.user)
        st.subheader('Add Tasks➕')
        st.dataframe(pd.DataFrame(st.session_state.tasks,columns=['Id','Task','Completed','Due date']).iloc[:,[1,2,3]],height=300,width=700)    
        
        #Add task
        new_task=st.text_input('Add Task: ',placeholder='Enter your Task',key='display')
        due_date=st.date_input('Due Date: ',format='DD/MM/YYYY')
        submit=st.form_submit_button('Add Task➕')
    
    if submit:
        if new_task and due_date:
            add_task(st.session_state.user,new_task,due_date)
            st.session_state.tasks=get_task(st.session_state.user)
            st.toast('Your Task Added',icon='✅')
            time.sleep(1.5)
            st.rerun()
        else:
            st.error('Enter some Task and due date...')
 
    df=pd.DataFrame(st.session_state.tasks,columns=['Id','Task','Completed','Due date'])
    df['status']=['Completed' if i==1 else 'Pending' for i in df['Completed']]
    count=df.groupby('status')['Completed'].count()
    count=pd.DataFrame(count).reset_index()
    if list(count.index):
        fig = px.pie(count, values="Completed", names="status",title="                  Task Status",height=500,width=700)
        st.sidebar.plotly_chart(fig)
    else:
        with st.sidebar:
            with st.container(border=True,height=200):
                st.write('** Task status will get updated here')



    st.title(' ')

    #Delete Task & complete task
    with st.container(border=True,height=600):
        st.subheader('Task Manager ⚙️')
        tasks=get_task(st.session_state.user)
        if tasks:
            choice=st.selectbox('Filter Tasks',options=['All','Completed','Pending','Today"s Tasks'])
            if choice=='Completed':
                tasks=[task  for task in tasks if task[2]==1]
            elif choice=='Pending':
                tasks=[task  for task in tasks if task[2]==0]
            elif choice=='Today"s Tasks':
                tasks=[task for task in tasks if task[3]==str(datetime.date.today())]
            
            col1,col2,col3,col4=st.columns([0.8,0.5,0.5,1])
            with col1:
                    st.write('#### Task')
            with col2:
                st.write('#### Status')
            with col3:
                st.write('#### Complete')
            with col4:
                st.write('#### Due date')
            for task in tasks:
                col1,col2,col3,col4,col5=st.columns([2,1,1,1,1])
                with col1:
                    st.write(task[1])
                with col2:
                    st.write('##### ✅' if task[2] else '##### 🕒')

                with col3:
                    if not(task[2]):
                        if st.button(f'☑️',key=f'complete_{task[0]}'):
                            complete_task(task[0])
                            st.session_state.tasks=get_task(st.session_state.user) 
                            st.toast('Task completed',icon='☑️')
                            time.sleep(1.5)
                            st.rerun()                  
                with col4:
                    st.write(f'{task[3]}')

                with col5:
                    if st.button(f'Delete',key=f'{task[0]}'):
                        delete_task(task[0])
                        st.toast('Task Deleted',icon='🗑️')
                        st.session_state.tasks=get_task(st.session_state.user)
                        time.sleep(1.5)
                        st.rerun()
        else:
            st.error('No tasks Found add some Tasks!')
        

    #download
    # st.write()
    csv=df.iloc[:,[1,3,4]].to_csv().encode("utf-8")
    st.download_button('Download your Tasks ⬇️',data=csv,file_name='Todo.csv',mime='text/csv')
        

if st.session_state.logged_in:       
    if st.sidebar.button('↩️ Logout'):
        st.session_state.logged_in=False
        st.session_state.pop('tasks')
        st.rerun()

        

    

    
