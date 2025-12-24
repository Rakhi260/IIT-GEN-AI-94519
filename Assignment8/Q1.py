from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
from langchain.agents.middleware import wrap_model_call
import os
import json
import requests

# ------------------ ENV ------------------
load_dotenv()


@wrap_model_call
def model_logging(request, handler):
    print("Before model call:",'-'*20)
    print(request)
    response = handler(request)
    print("After model call:",'-'*20)
    print(response)
    response.result[0].content = response.result[0].content.upper()
    return response

@wrap_model_call
def limit_model_context(request, handler):
    print("*Before model call: ",'-'*20)
    #print(request)
    request.messages = request.messages[-5:]
    response = handler(request)
    print("*After model call:",'-'*20)
    print(response)
    response.result[0].content = response.result[0].content.upper()
    return response

# ------------------ TOOLS ------------------
@tool
def calculator(expression: str) -> str:
    """
    Evaluates a basic arithmetic expression and returns the result.
    Supports +, -, *, / and parentheses.
    """
    try:
        return str(eval(expression))
    except Exception:
        return "Error: Invalid arithmetic expression"


@tool
def get_weather(city: str) -> str:
    """
    Fetches the current weather of a given city using OpenWeather API.
    Returns weather data in JSON string format.
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )
        response = requests.get(url)
        return json.dumps(response.json())
    except Exception:
        if response.status_code == 200:
             return json.dumps(response.json())
        else:
             return "Error fetching weather"



@tool
def read_file(filepath: str) -> str:
    """
    Reads a text file from the given file path and returns its content.
    """
    with open(filepath, "r") as file:
        return file.read()
    
@tool
def knowledge_lookup(query: str) -> str:
    """
    Looks predefined knowledge based on query
    """
    knowledge_base = {
        "python": "Python is a high-level programming language.",
        "langchain": "LangChain helps build LLM-powered applications.",
        "lm studio": "LM Studio runs LLMs locally on your machine."
    }

    return knowledge_base.get(query.lower(), "No knowledge found.")

# ------------------ MODEL ------------------
llm = init_chat_model(
    model="google_gemma-3-4b-it",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

# ------------------ AGENT ------------------
agent = create_agent(
    model=llm,
    tools=[calculator, get_weather, read_file,knowledge_lookup],
    middleware = [model_logging, limit_model_context],
    system_prompt="You are a helpful assistant. Answer briefly and clearly."
)

# ------------------ CHAT LOOP ------------------
conversation = []
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    
    conversation.append({"role":"user","content":user_input})

    response = agent.invoke({
        "messages": conversation
    })
    
    conversation = response["messages"]

    print("AI:", conversation[-1].content)