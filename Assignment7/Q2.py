# # Create a Streamlit application that takes a city name 
# # as input from the user.Fetch the current weather using
# # a Weather API and use an LLM to explain the weather conditions 
# # in simple English.

# import requests
# import os
# import streamlit as st
# from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model

# load_dotenv()

# llm = init_chat_model(
#     model = "llama-3.3-70b-versatile",
#     model_provider = "openai",
#     base_url = "https://api.groq.com/openai/v1",
#     api_key = os.getenv("GROQ_API_KEY")
# )

# st.title("Weather chatbot")
# city = st.text_input("Enter city")

# if st.button("Get Weather"):
#     if not city:
#         st.write("im here,city not found")
#         st.warning("Please enter avalid city")
#         st.stop()
        
#         weather_api = os.getenv("OPENWEATHER_API_KEY")
#         url = (
#             "https://api.openweathermap.org/data/2.5/weather"
#             f"?appid={api_key}&units=metric&q={city}"
#         )
#         response = request.get(url)
#         st.write("im here,request sent")
        
#         if response.status_code == 200:
#             data = response.json()

#         temp = data["main"]["temp"]
#         humidity = data["main"]["humidity"]
#         condition = data["weather"][0]["description"]

#         # Display raw weather data
#         st.subheader("Current Weather Data")
#         st.write(f"Temperature: {temp} °C")
#         st.write(f"Humidity: {humidity}%")
#         st.write(f"Condition: {condition}")

#         # LLM prompt
#         prompt = f"""
#         Explain today's weather in {city} in very simple English.

#         Temperature: {temp} °C
#         Humidity: {humidity} %
#         Condition: {condition}
#         """

#         explanation = llm.invoke(prompt)

#         st.subheader("Weather Explanation")
#         st.write(explanation.content)

#     else:
#         st.error("City not found or API error")


import streamlit as st
import time
from langchain.chat_models import init_chat_model
import os
import requests

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="http://127.0.0.1:1234",
    api_key=os.getenv("dummy")
)

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()

st.title("Weather Explanation Assistant")

city = st.text_input("Enter city name")

if st.button("Get Weather Explanation") and city:

    data = get_weather(city)
    if data is None:
        st.error("City not found!")
    else:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]

        llm_input = f"""
        City: {city}
        Temperature : {temp} in Celsius
        Humidity : {humidity} %
        Wind Speed : {wind} m/s
        Description : {desc}

        Instruction: Give explanation in simple English in 7 sentences.
        """

        st.subheader("AI Explanation")

        output_box = st.empty()
        final_text = ""

        for chunk in llm.stream(llm_input):
            final_text += chunk.content
            output_box.write(final_text)
            time.sleep(0.05)