#Q1: Design a Streamlit-based application with a sidebar
# to switch between Groq and LM Studio. The app should 
# accept a user question and display responses using Groq’s
# cloud LLM and a locally running LM Studio model.Also
# maintain and display the complete chat history of user questions and model responses.

import streamlit as st
from langchain.chat_models import init_chat_model 
import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "model" not in st.session_state:
    st.session_state.model = []
    
with st.sidebar:
    st.header("Model Switch")
    select_model = st.radio("Choose LLM",["Groq","LM Studio"])
    st.session_state.model = select_model
    st.write(f"**Active Model:** {select_model}")
    
 #functions   
def call_groq(user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": user_message}]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]


def call_lm_studio(user_message):
    url = "http://localhost:1234/v1/chat/completions"

    payload = {
        "model": "phi-3.1-mini-4k-instruct",
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return "LM Studio server not running"

# UI 
st.title("Chatbot")

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# User input
user_input = st.chat_input("Hello!! Whats on your mind today")

if user_input:
    # Show user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # Model response
    with st.chat_message("assistant"):
        if st.session_state.model == "Groq":
            response = call_groq(user_input)
        else:
            response = call_lm_studio(user_input)

        st.write(response)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": response}
    )
   
        
        



    

