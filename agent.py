import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# 1. Load the hidden API key from our .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Initialize the official Google GenAI Client
client = genai.Client(api_key=api_key)

print("🤖 Super-Parsing Multimodal AI Agent Initialized!")
print("• Drag & drop an image or paste the path with quotes!\n")

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a brilliant assistant. Look at the image provided and answer the user's question clearly.",
        tools=[{"google_search": {}}]
    )
)

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ['exit', 'quit']:
        print("🤖 Agent: Goodbye!")
        break
        
    if not user_input:
        continue

    try:
        if user_input.startswith("/image "):
            # Clean up the command line text
            cmd_content = user_input.replace("/image ", "").strip()
            
            # Smart Regex: Find a path inside quotes, or take up to the file extension
            match = re.match(r'^"([^"]+)"(.*)|^\'([^\']+)\'(.*)', cmd_content)
            
            if match:
                # If the user used quotes
                image_path = match.group(1) or match.group(3)
                text_prompt = match.group(2) or match.group(4)
            else:
                # If no quotes, look for common image extensions to find where the path ends
                split_match = re.search(r'(.*?\.(?:png|jpg|jpeg|webp|gif))(.*)', cmd_content, re.IGNORECASE)
                if split_match:
                    image_path = split_match.group(1)
                    text_prompt = split_match.group(2)
                else:
                    print("❌ Error: Could not parse image path. Make sure it ends in .png or .jpg\n")
                    continue

            image_path = image_path.strip()
            text_prompt = text_prompt.strip() if text_prompt.strip() else "Describe this image."

            if os.path.exists(image_path):
                img = Image.open(image_path)
                print("🔄 Analyzing image pixels...")
                response = chat.send_message([img, text_prompt])
                print(f"🤖 Agent: {response.text}\n")
            else:
                print(f"❌ Error: File not found at '{image_path}'.\n")
                
        else:
            response = chat.send_message(user_input)
            print(f"🤖 Agent: {response.text}\n")
            
    except Exception as e:
        print(f"⚠️ An error occurred: {e}\n")