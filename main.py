from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()
print(os.getenv("GROQ_API_KEY"))

# llm = ChatGroq(model="qwen/qwen3.8-27b")