from dotenv import load_dotenv
load_dotenv() ## load all env variables.

import  streamlit as st
import os 
import sqlite3

import google.generativeai as genai

## config gen ai key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load genai(gemini) model and give queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0], question])
    return response.text

# Function to retrive query from sql database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    if not rows:
        return []
    return rows
    
## Define your prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION
    \n\nFor example,\nExample 1 -  How many entries of record are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 -  Tell me all the students studying in Software engineering class?,
    the SQL command will be something like this SELECT * FROM STUDENT where CLASS='Software engineering';
    also the sql code should not have ``` in beginning or end and sql word in output
    give response in a textual format without ()/' or , .
    
    """
]

# Streamlit app

st.set_page_config(page_title="Use me to retrieve any  SQL query")
st.header("Gemini App to retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit=st.button("Ask the question")

# if submit is clicked

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("Here's your answer")
    if response:
        for row in response:
            print(row)
            st.write(row)
    else:
        st.write("No results found.")