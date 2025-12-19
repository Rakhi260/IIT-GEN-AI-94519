from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")
# llm = ChatGroq(model = "openai/gpt-oss-120b", api_key=api_key)

api_key = os.getenv("GEMINI-API")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=api_key
)

user = input("You: ")

result = llm.invoke(user)
print("AI:",result.content)

# result = llm.stream(user)
# for chunk in result:
#     print(chunk.content, end="")
