import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load the hidden API key from our .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize the official Google GenAI Client
client = genai.Client(api_key=api_key)

print("🤖 Custom AI Agent Initialized!")
print("Type 'exit' or 'quit' to stop chatting.\n")

# 3. Start an interactive chat session with custom instructions
# You can change the system_instruction below to give your agent a different personality!
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a witty, highly intelligent coding assistant. Keep your responses crisp and helpful."
    )
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("🤖 Agent: Goodbye!")
        break
        
    if not user_input.strip():
        continue

    # Send the message to the agent and stream the response back
    response = chat.send_message(user_input)
    print(f"🤖 Agent: {response.text}\n")