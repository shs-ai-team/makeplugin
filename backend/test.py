import os
from dotenv import load_dotenv
from openai import OpenAI

# loading environment variables from the .env file
load_dotenv()

# setting api key and base url
api_key = os.getenv("AIML_API_KEY")
base_url = "https://api.aimlapi.com/v1"

# A robust check to ensure the API key is set
if not api_key:
    raise ValueError("API key not found. Please set the AIML_API_KEY environment variable or create a .env file.")

# print("api-key is ", api_key)

system_prompt = "You are a travel agent. Be descriptive and helpful."
user_prompt = "Tell me about Barcelona"

# Fix for Gemma model that does not suport system messages
# We combine the two prompts into one for such smaller models
combined_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

api = OpenAI(api_key=api_key, base_url=base_url)


def main():
    completion = api.chat.completions.create(
        model="openai/gpt-5-2025-08-07",

        # Version with both system and user prompt
        # messages=[
        #     {"role": "system", "content": system_prompt},
        #     {"role": "user", "content": user_prompt},
        # ],

        # Version with combined prompt for gemma and other smaller models
        messages=[
            # Verwende nur die Rolle "user" mit dem kombinierten Prompt
            {"role": "user", "content": combined_prompt},
        ],

        temperature=0.7,
        max_tokens=500,
    )

    response = completion.choices[0].message.content

    print("User:", user_prompt)
    print("AI:", response)


if __name__ == "__main__":
    main()