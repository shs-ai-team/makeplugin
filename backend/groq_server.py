# groq_test.py
import asyncio
from openai import AsyncOpenAI
from prompt_config import SYSTEM_PROMPT
import os # NEW: To get the API key from .env
from dotenv import load_dotenv
load_dotenv()

# --- Configuration for Groq Cloud ---

# 1. Add your Groq API Key to your .env file like this:
# GROQ_API_KEY="gsk_YourSecretKey..."

client = AsyncOpenAI(
    # 2. UPDATED: Use Groq's endpoint
    base_url="https://api.groq.com/openai/v1", 
    # 3. UPDATED: Use the Groq API key from your .env file
    api_key=os.getenv("GROQ_API_KEY"),
)

# 4. UPDATED: Use a model name available on Groq (e.g., Llama 3)
MODEL_NAME = "llama3-8b-8192"

async def test_groq_model():
    print(f"--- Testing Groq model: {MODEL_NAME} ---")

    user_prompt = "Create a simple plugin that adds a shortcode [hello_world] to display the text 'Hello World'."
    
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
        )
        
        generated_json = response.choices[0].message.content
        
        print("\n--- SUCCESS ---")
        print("AI JSON Response from Groq:")
        print(generated_json)

    except Exception as e:
        print("\n--- ERROR ---")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Make sure to add your GROQ_API_KEY to your .env file
    asyncio.run(test_groq_model())