import streamlit as st
from langchain.chat_models import init_chat_model
import pandas as pd
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
import chromadb
import tempfile

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

embed_model = init_embeddings (
    model = "text-embedding-nomic-embed-text-v1.5" ,
    provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "not-needed",
    check_embeddings_ctx_length=False
)

client = chromadb.Client()
collection = client.get_or_create_collection(name="resumes")


if "conversation" not in st.session_state:
    st.session_state.conversation = []

#streamlit ui  
st.title("Resume Manager")

menu = st.sidebar.selectbox(
    "Menu",
    ["Upload Resume","List Resumes","Delete Resumes","Shortlist Resumes"]
)

data_file = st.file_uploader("Upload a CSV file",type=["csv","pdf"])

def load_pdf_resume(data_file):
    loader = PyPDFLoader(data_file)
    docs = loader.load()
    resume_content = ""
    for page in docs:
        resume_content += page.page_content
    metadata = {
        "source" : data_file,
        "page_count" : len(docs)
    }
    
    return resume_content,metadata

resume_text, resume_info = load_pdf_resume(data_file)
print(resume_info)
print(resume_text)
    
user = st.chat_input("Say something")
if user:
    st.session_state.conversation.append(
        {"role": "user", "content": user}
    )

    context = st.session_state.conversation

    response = llm.invoke(context)

    st.session_state.conversation.append(
        {"role": "assistant", "content": response.content}
    )
    
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
    



