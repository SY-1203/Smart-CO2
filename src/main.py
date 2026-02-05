from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv()
api_key = os.getenv("APIKey")
if not api_key:
    raise ValueError("API Key not found in .env file")

# Create Groq client
client = Groq(api_key=api_key)
client = Groq(api_key=api_key)

chat = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello World!"}]
)

print(chat.choices[0].message.content)


