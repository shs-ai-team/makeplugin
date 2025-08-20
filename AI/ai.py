from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class AI:
    aiml_api_key = os.getenv("AIML_API_KEY")
    aiml_base_url = os.getenv("AIML_API_BASE_URL")
    api = OpenAI(
        api_key=aiml_api_key,
        base_url=aiml_base_url,
    )

    @classmethod
    def get_response(cls, messages):
        completion = cls.api.chat.completions.create(
            model="openai/gpt-5-2025-08-07",
            messages=messages,
            temperature=0.2,
            verbosity="high"
        )
        response = completion.choices[0].message.content
        return response
    
    