from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

aiml_api_key = os.getenv("AIML_API_KEY")
aiml_base_url = os.getenv("AIML_API_BASE_URL")
print("Loded API config:\nAIML API Key:", aiml_api_key, "\nAIML Base URL:", aiml_base_url)

system_prompt = "You are a helpful AI assistant that replies consisely in one or few words, never more than a sentence."
# user_prompt = "What are the minimum requirements to completely define a simple wordpress plugin?"
user_prompt = input("User: ")

while user_prompt.strip() != "":
    print("Calling AI...")
    api = OpenAI(
        api_key=aiml_api_key,
        base_url=aiml_base_url,
    )
    completion = api.chat.completions.create(
        model="openai/gpt-5-2025-08-07",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        # max_tokens=100,
        temperature=0.2,
        verbosity="high"
    )
    response = completion.choices[0].message.content
    print("AI: ", response)
    print()
    user_prompt = input("User: ")
