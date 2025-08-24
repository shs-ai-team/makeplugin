# from openai import OpenAI
# from dotenv import load_dotenv
# import os
import random
import json

# load_dotenv()

class AI:
    # api = OpenAI(
    #     api_key=os.getenv("AIML_API_KEY"),
    #     base_url=os.getenv("AIML_API_BASE_URL"),
    # )

    @classmethod
    def get_response(cls, messages):
        # completion = cls.api.chat.completions.create(
        #     model="openai/gpt-5-2025-08-07",
        #     messages=messages,
        #     temperature=0.2,
        #     verbosity="high"
        # )
        # response = completion.choices[0].message.content
        # return response
        dummy_choices = [
            """```json
{
    "requirements_clarified": false,
    "requirements": {},
    "response_to_user": "Please provide more details about the plugin you need."
}
```""",
            """```json
{
    "requirements_clarified": true,
    "requirements": {
        "plugin_name": "Example Plugin",
        "plugin_description": "This is an example plugin for demonstration purposes.",
        "additional_requirements": {}
    },
    "response_to_user": "Thank you for the details. I will now proceed with the plugin generation."
}
```"""
        ]
        return random.choice(dummy_choices)
    

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