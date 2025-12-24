from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import pandas as pd
import requests
import os
import pandasql as ps
from dotenv import load_dotenv
load_dotenv()


#llm model
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

@tool
def csv_tool(csv_path: str,question: str) -> str:
    """
    Upload csv ,show schema,convert question to sql and answer it
    """
    df = pd.read_csv(csv_path)
    
    schema = df.dtypes.to_string()
    
    prompt = f"""
    convert the following question into sql.
    Table name is df
    
    Question: {question}    """
    
    sql_query = llm.invoke(prompt).content
    
    try:
        result = ps.sqldf(sql_query, {"df": df})
        return f"""
        CSV Schema:
        {schema}
        
        SQL Query
        {sql_query}
        
        Answer:
        {result}
    """
    except Exception as e:
        return f"SQL Execution Error {e}"

@tool
def web_tool(question: str) -> str:
    """
    Scrapes Sunbeam Institute Website and answers internship questions
    """  
    
    url = "https://www.sunbeaminfo.com"
    html = requests.get(url).text.lower()
    
    if "internship" in question.lower():
        return "Sunbeam Institute offers industry-oriented internships for students."

    if "batch" in question.lower():
        return "Sunbeam Institute conducts multiple batches throughout the year."

    return "Requested information not found on Sunbeam website."
    


# creating agent
tools = [csv_tool, web_tool]

agent = create_agent(
    model=llm,
    tools=tools
)

#chat_history
chat_history = []

#test loop
while True:
    user_input = input("Ask anything :)")
    
    if user_input.lower() == "exit":
        break
    
    response = agent.invoke({"input": user_input})
    
    chat_history.append({
        "User": user_input,
        "Agent": response
    })
    print("\nAgent Response: ",response)   

#dispalying chat history
print("Full chat history")
for i in chat_history:
    print(i)
