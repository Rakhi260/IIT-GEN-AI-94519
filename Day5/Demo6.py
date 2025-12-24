# Input city name from user.
# Get current weather from weather API.
# Ask LLM to explain the weather in English.

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import streamlit as st
import requests
import os
load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)
conversation = [
    {"role": "system", "content": "You are SQLite expert developer with 10 years of experience."}
]

st.title("Weather App")
city = st.text_input("Enter city name: ")

if st.button("Get Weather"):
        api_key= os.getenv("OPENWEATHER_API_KEY")
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}")
        response = requests.get(url)
        st.write("status:", response.status_code)
        
        if response.status_code == 200:
            data = response.json()
            
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]
            
            prompt = f""" Explain todays weather in {city} in simple engish language.condition
            Temperature is {temp} degree celsius,
            Humidity is {humidity} percent
            and condition is {condition} """
            
            explanation = llm.invoke(prompt)
                        
            st.subheader("Weather Application")
            st.write(explanation.content)
        
        else:
         st.error("City not found")
                      
                      