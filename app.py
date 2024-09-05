from dotenv import load_dotenv
load_dotenv() ## load all env variables.

import  streamlit as st
import os 
import sqlite3

import google.generativeai as genai

def connect_to_database(db_path):
    # debugging
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Running a test query
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("Connection successful. Found tables:", tables)
        else:
            print("Connection successful but no tables found.")
        
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
# User database upload func
def upload_and_connect():
    uploaded_file = st.file_uploader("Upload your own SQLite database Note: Make sure to upload it with .db extension", type="db")
    if uploaded_file is not None:
        with open("user_db.db", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Database uploaded successfully!")
        return connect_to_database("user_db.db")
    else:
        return None
    
# Connecting to the database(initial/default database)
db_connection = connect_to_database('multiinfo.db')

st.set_page_config(layout="wide")
BOT_LOGO = "./image.png"
# MODEL_AVATAR_URL = "./hero.png"

## config gen ai key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)       
                

# Descriptions and example queries for each page
page_descriptions = {
    "Property Records": {
        "description": """
        This section allows you to query property records. You can find information about different properties, including owner details, market value,type of property and more.
        """,
        "example_query": "Show me all commercial properties in Pune"
    },
    "Healthcare Records": {
        "description": """
        This section allows you to query healthcare records. You can find information about patients assigned to doctors, diagnoses, treatments, and more.
        """,
        "example_query": "Give me the name of patients who are suffering from Asthma"
    },
    "Finance Records": {
        "description": """
        This section allows you to query finance records. You can find information about investments, returns, maturity dates, and more.
        """,
        "example_query": "Which assest gives the best ROI from the FinanceRecords database"
    }
}

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Property Records", "Healthcare Records", "Finance Records"])

st.title("Multitask Pro: AI-Powered Data Retrieval SQL-GPT")
st.markdown(page_descriptions[page]["description"])
st.markdown(f"**Example Query:** {page_descriptions[page]['example_query']}")

# Database upload section
st.sidebar.title("Upload your database")
uploaded_db_connection = upload_and_connect()
if uploaded_db_connection:
    db_connection = uploaded_db_connection

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def clear_chat_history():
    st.session_state["messages"] = []

st.button('Clear Chat', on_click=clear_chat_history)

# Function to generate SQL query
def generate_sql_query(user_input):
    prompt = f"Generate an SQL query to find information based on the user's question: '{user_input}'. Note: The table names are 'PropertyRecords', 'HealthcareRecords', 'FinanceRecords' and the columns are 'PropertyID', 'OwnerName', 'Address', 'City', 'State', 'Zipcode', 'PropertyType', 'MarketValue', 'LastSoldDate' for PropertyRecords; 'RecordID', 'PatientName', 'Age', 'Gender', 'Diagnosis', 'Treatment', 'DoctorName', 'VisitDate' for HealthcareRecords; 'RecordID', 'InvestorName', 'InvestmentType', 'AmountInvested', 'ROI', 'InvestmentDate', 'MaturityDate' for FinanceRecords. Note: Give the query without '''sql at the start and end of the query. just give the query text content."
    response = model.generate_content(prompt)
    print(response.text)
    return response.text 

def execute_sql_query(query):
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        print(results)
        return results
    except Exception as e:
        return f"Error executing query: {str(e)}"

def format_response(user_input, query_results):
    if not query_results:
        return "No data found for your query."

    result_text = f"Found {len(query_results)} results: " + ', '.join([str(item) for sublist in query_results for item in sublist])
    
    prompt = f"Rephrase this in a more conversational and informative way based on the user's question: '{user_input}'. Here are the details: {result_text}. Answer the user's question in a conversational manner. Note: as its a conversational response, give the response in correct mannser with correct formatting"
    formatted_response = model.generate_content(prompt)
    print(formatted_response.text)
    return formatted_response.text

def handle_user_input(user_input):
    with history:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate SQL query from user input
        sql_query = generate_sql_query(user_input)
        if sql_query:
            # Execute the generated SQL query
            query_results = execute_sql_query(sql_query)
            formatted_answer = format_response(user_input, query_results)
            
            # with st.chat_message("assistant", avatar=BOT_LOGO):
            #     st.markdown(formatted_answer)
            st.session_state["messages"].append({"role": "assistant", "content": formatted_answer})
        else:
            # with st.chat_message("assistant", avatar=BOT_LOGO):
            #     st.markdown("Failed to generate a valid SQL query.")
                st.session_state["messages"].append({"role": "assistant", "content": "Failed to generate a valid SQL query."})

# # Forcing a rerun to display the new message immediately
#     st.experimental_rerun()

main = st.container()
with main:
    history = st.container(height=400)
    with history:
        for message in st.session_state["messages"]:
            avatar = BOT_LOGO if message["role"] == "assistant" else None
            with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

    if prompt := st.chat_input("Type your question:", max_chars=1000):
        handle_user_input(prompt)
 


# initial code to test gemini (IGNORE)
 
# Function to load genai(gemini) model and give queries as response

# def get_gemini_response(question,prompt):
#     model=genai.GenerativeModel('gemini-pro')
#     response=model.generate_content([prompt[0], question])
#     return response.text

# # Function to retrive query from sql database

# def read_sql_query(sql,db):
#     conn=sqlite3.connect(db)
#     cur=conn.cursor()
#     cur.execute(sql)
#     rows=cur.fetchall()
#     conn.commit()
#     conn.close()
#     if not rows:
#         return []
#     return rows
    
# ## Define your prompt
# prompt=[
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name PropertyRecords and has the following columns - NAME, CLASS, SECTION
#     \n\nFor example,\nExample 1 -  How many entries of record are present?,
#     the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
#     \nExample 2 -  Tell me all the students studying in Software engineering class?,
#     the SQL command will be something like this SELECT * FROM STUDENT where CLASS='Software engineering';
#     also the sql code should not have ``` in beginning or end and sql word in output
#     give response in a textual format without ()/' or , .
    
#     """
# ]

# # Streamlit app

# st.set_page_config(page_title="Use me to retrieve any  SQL query")
# st.header("Gemini App to retrieve SQL Data")

# question = st.text_input("Input: ", key="input")

# submit=st.button("Ask the question")

# # if submit is clicked

# if submit:
#     response=get_gemini_response(question,prompt)
#     print(response)
#     response=read_sql_query(response,"property.db")
#     st.subheader("Here's your answer")
#     if response:
#         for row in response:
#             print(row)
#             st.write(row)
#     else:
#         st.write("No results found.")