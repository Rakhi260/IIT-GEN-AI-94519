from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

# ------------------ ENV ------------------
load_dotenv()

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
        return "Error: Unable to fetch weather"


@tool
def read_file(filepath: str) -> str:
    """
    Reads a text file from the given file path and returns its content.
    """
    with open(filepath, "r") as file:
        return file.read()

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
    tools=[calculator, get_weather, read_file],
    system_prompt="You are a helpful assistant. Answer briefly and clearly."
)

# ------------------ CHAT LOOP ------------------
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    print("AI:", response["messages"][-1].content)