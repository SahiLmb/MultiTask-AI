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
    
# Connecting to the database
db_connection = connect_to_database('multiinfo.db')

st.set_page_config(layout="wide")
BOT_LOGO = "./image.png"
# MODEL_AVATAR_URL = "./hero.png"

## config gen ai key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
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
                

DESCRIPTION = """
This app leverages the power of AI to transform natural language inputs into SQL queries, 
enabling users to interact with a database effortlessly. Designed specifically for public records management, 
it allows users to query property, healthcare, and finance records and receive responses in natural language, making data retrieval intuitive 
and user-friendly.\n
How It Works \n
- User Input: The user types a plain language query, such as "Show me all residential properties in Mumbai or give me patients who are under Dr. verma or give the number of people invested in stocks."\n
- NLP Conversion: Advanced AI models convert the user's input into a SQL query.\n
- Database Execution: The SQL query is executed on the property records database.\n
- Data Retrieval: Relevant data is fetched from the database.\n
- Natural Language Response: The data is formatted into a conversational response and displayed to the user.
"""

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Property Records", "Healthcare Records", "Finance Records"])

st.title("Multitask Pro: AI-Powered Data Retrieval SQL-GPT")
st.markdown(DESCRIPTION)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def clear_chat_history():
    st.session_state["messages"] = []

st.button('Clear Chat', on_click=clear_chat_history)

# Function to generate SQL query
def generate_sql_query(user_input):
    prompt = f"Generate an SQL query to find information based on the user's question: '{user_input}'. Note: The table names are 'PropertyRecords', 'HealthcareRecords', 'FinanceRecords' and the columns are 'PropertyID', 'OwnerName', 'Address', 'City', 'State', 'Zipcode', 'PropertyType', 'MarketValue', 'LastSoldDate' for PropertyRecords; 'RecordID', 'PatientName', 'Age', 'Gender', 'Diagnosis', 'Treatment', 'DoctorName', 'VisitDate' for HealthcareRecords; 'RecordID', 'InvestorName', 'InvestmentType', 'AmountInvested', 'ROI', 'InvestmentDate', 'MaturityDate' for FinanceRecords. Note: Give the query without '''sql at the start and end of the query. just give the query text content"
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
            
            with st.chat_message("assistant", avatar=BOT_LOGO):
                st.markdown(formatted_answer)
                st.session_state["messages"].append({"role": "assistant", "content": formatted_answer})
        else:
            with st.chat_message("assistant", avatar=BOT_LOGO):
                st.markdown("Failed to generate a valid SQL query.")
                st.session_state["messages"].append({"role": "assistant", "content": "Failed to generate a valid SQL query."})

main = st.container()
with main:
    history = st.container(height=400)
    with history:
        for message in st.session_state["messages"]:
            avatar = None
            if message["role"] == "assistant":
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