from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import requests
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

user_input = input("Enter message : ")
data = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": user_input}
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print("Status:", response.status_code)

result = response.json()


if response.status_code == 200 and "choices" in result:
    print(result["choices"][0]["message"]["content"])
else:
    print("API Error Response:")
    print(result)