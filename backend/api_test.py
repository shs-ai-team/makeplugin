# api_test.py
import os
import asyncio
from openai import AsyncOpenAI, APIError
from dotenv import load_dotenv

load_dotenv()

async def test_api_connection():
    print("--- Starting API Connection Test ---")
    
    api_key = os.getenv("AIML_API_KEY")
    base_url = "https://api.aimlapi.com/v1"
    model = "openai/gpt-5-2025-08-07" # Test with the smaller model

    if not api_key:
        print("ERROR: AIML_API_KEY not found in .env file.")
        return

    print(f"Using Model: {model}")
    print(f"Using Base URL: {base_url}")

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello, who are you?"}]
        )
        print("\n--- SUCCESS ---")
        print("AI Response:", response.choices[0].message.content)

    except APIError as e:
        print("\n--- API ERROR ---")
        print(f"Status Code: {e.status_code}")
        print(f"Error Message: {e.message}")
        print(f"Full Response Body: {e.body}")
    
    except Exception as e:
        print("\n--- GENERAL ERROR ---")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_api_connection())