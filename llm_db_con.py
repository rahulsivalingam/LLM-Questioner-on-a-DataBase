import streamlit as st

st.set_page_config(
    page_title = "Querying DB",
    layout = "centered"

)

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import create_react_agent
import time 
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
import psycopg2
from sqlalchemy.exc import OperationalError

import os
os.environ['OPENAI_API_KEY'] = ''
os.environ['SERPAPI_API_KEY'] = ''

llm = OpenAI(temperature = 0)
tools = load_tools(['serpapi', 'llm-math'], llm = llm)

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

def createconnection(db_user,db_password,db_name,db_port):

    db_host = 'database-1.cv2ekosyw420.eu-north-1.rds.amazonaws.com'

    db_uri = (f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    #db = SQLDatabase.from_uri(db_uri)
    try:
        db = SQLDatabase.from_uri(db_uri)
        db.get_usable_table_names()
        #print("succcessful Connection to DB")
        return db

    except Exception as e:
        print(f"Failed to connect due to {e}")
        return None

    except OperationalError as e:
        print(f"failed due to {e}")
        return None



from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name = 'gpt-3.5-turbo')

def getquery(question, db):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose = True
    )

    response = agent_executor.run(question)
    return response



#response = getquery(question)



##################.  STREAMLIT FRONTEND ################




with st.sidebar:
    st.title("Connect to DB")
    db_user = st.text_input(label = 'User', key = 'db_user', value = 'postgres')
    db_password = st.text_input(label = 'password', key = 'db_password', value = 'postgres', type = 'password')
    db_name = st.text_input(label = 'Databse Name', key = 'db_name', value = 'postgres')
    db_port = st.text_input(label = 'Port', key = 'db_port', value = '5432')
    connectbtn = st.button("Connect")

if "db" not in st.session_state:
    st.session_state.db = None

if connectbtn:
    #createconnection()
    st.session_state.db = createconnection(        
        db_user=db_user,
        db_password=db_password,
        db_name=db_name,
        db_port=db_port
        )
    if st.session_state.db:
        st.success("Database Connected")

if "chat" not in st.session_state:
    st.session_state.chat = []

question = st.chat_input("What do you want to ask the DB")

if question:
    if not st.session_state.db:
        st.error("No connection to the DB Connec to the DB first and then try")
    else:
        st.session_state.chat.append({
            "role":"user",
            "content": question
        })
        #st.chat_message("user").markdown(question)
        response = getquery(question, st.session_state.db)
        #st.chat_message("asistant").markdown(response)
        st.session_state.chat.append({
            "role":"assistant",
            "content": response
        })

for chat in st.session_state.chat:
    st.chat_message(chat['role']).markdown(chat['content'])

        




# how many tables in the databse
# how many records are there in the t shirt table
# what are the different colour and sized of t shirts in the table 
# is there a discount on the black tshirts  
# what is the largest size of the blue tshirt 
# if i buy a white tshirt of size s, do i get a discount