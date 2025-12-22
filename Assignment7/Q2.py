# Create a Streamlit application that takes a city name 
# as input from the user.Fetch the current weather using
# a Weather API and use an LLM to explain the weather conditions 
# in simple English.

import requests
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model = "gemma-3-4b-it",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1" ,
    api_key = os.getenv("GROQ_API_KEY")
)

st.title("Weather chatbot")
city = st.text_input("Enter city")

if st.button("Get Weather"):
    st.write("im here,inside")
    if not city:
        st.write("im here,city not found")
        st.warning("Please enter avalid city")
        st.stop()
        
        weather_api = os.getenv("OPEN_WEATHER_API")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = request.get(url)
        st.write("im here,request sent")
        
        if response.status_code == 200:
            data = response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]

        # Display raw weather data
        st.subheader("Current Weather Data")
        st.write(f"Temperature: {temp} °C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Condition: {condition}")

        # LLM prompt
        prompt = f"""
        Explain today's weather in {city} in very simple English.

        Temperature: {temp} °C
        Humidity: {humidity} %
        Condition: {condition}
        """

        explanation = llm.invoke(prompt)

        st.subheader("Weather Explanation")
        st.write(explanation.content)

    else:
        st.error("City not found or API error")