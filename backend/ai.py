from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class AI:
    api = OpenAI(
        api_key=os.getenv("AIML_API_KEY"),
        base_url=os.getenv("AIML_API_BASE_URL"),
    )

    @classmethod
    def get_response(cls, messages):
        
        # Adjust messages to OpenAI format
        for idx, message in enumerate(messages):
            messages[idx] = {

                "role": message["role"]\
                    .replace("consultant", "assistant")\
                    .replace("developer", "assistant"),
                    
                "content": message["content"],
            }

        print("LOG: calling AI with following messages:")
        print(f"LOG: {list((messages))}")

        completion = cls.api.chat.completions.create(
            model="openai/gpt-5-2025-08-07",
            messages=messages,
            temperature=0.2,
            verbosity="high",
            max_completion_tokens=10000
        )
        response = completion.choices[0].message.content
        print("LOG: Receieved AI response:")
        print(f"LOG: {completion}")

        return response    

    @classmethod
    def get_response_plugin_generation(cls, requirements):
        """
        Dummy response for plugin file generation.
        Returns JSON with file names and contents.
        """
        dummy_response = {
            "files": {
                "example-plugin.php": "<?php\n/* Plugin Name: Example Plugin */\n\n// Your plugin code here\n",
                "readme.txt": "This is a dummy readme for the Example Plugin."
            },
            "success": True,
        }
        return json.dumps(dummy_response)