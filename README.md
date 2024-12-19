# LLM-Questioner-on-a-DataBase

The main aim of this project is to create and LLM model that can query a database using natural language instead of writing SQL queries. 

The project uses the LangChain agents and OpenAI’s language model to translate natural language into SQL queries that is to be queried against a database. LangChain is a framework for building language models applications and uses tools and agents to process natural language into SQL queries. GPT models from OpenAI are used to process the user input and generate responses. 

An OPENAI_API_KEY is used for authentication with OpenAI and a SERP_API_KEY give access to real time search engine data rather than requiring to manually scrape web pages. SerpAPI is beyond the scope of this project. 


Workflow:

The environment is first set up with the help of the OPENAI_API_KEY.  This is essential for enabling OpenAI and LangChain functionalities. 

The PostGres database is now connected with the help of parametrs taken from a user input like the db_user, db_password, db_name and db_port. The code is initialized with default values but the user is free to connect to the Database of their choice. We get a status message upon the successful connection with the database. 

The LLM is initialized with the help of the ChatOpenAI using the “gpt-3.5-turbo” model. There are numerous model supported by OpenAI but this was used for the sake of simplicity and is one among the many supported in the current payment tier of OpenAI. A toolkit using the SQLDatabaseToolkit is created to interact with the database and a SQL agent is created to create these SQL queries with the help of the previously initialized LLM. An agent_executor is then used to run these queries against the database taking the queries in the form of natural language from the user, and the result is then displayed to the user in natural language. 

Streamlit is used as the front end for this application where the user enters the database connection info, open successful connection, the query is entered in natural language, which is then processes and the user receives the result in a natural language. All queries are stored and displayed to the user in the form a chat till the session is cleared. 



 


![image](https://github.com/user-attachments/assets/830a9228-2c9c-4c5b-ad3d-b91e8c59e97c)
