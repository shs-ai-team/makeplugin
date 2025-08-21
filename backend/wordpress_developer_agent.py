import json
from ai import AI
from prompts import wordpress_developer_agent_system_prompt, wordpress_developer_agent_user_prompt

class WordpressDeveloperAgent:

    def __init__(self, requirements):
        self.requirements = requirements  # JSON reqs from consultant agent

    def generate_plugin_files(self):

        user_message = wordpress_developer_agent_user_prompt.format(
            plugin_requirements=json.dumps(self.requirements, indent=2)
        )

        messages = [
            {"role": "system", "content": wordpress_developer_agent_system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = AI.get_response_plugin_generation(messages)

        # Parse response

        # Find the '## Plugin Files' section
        response = response.strip().split("## Plugin Files")
        try:
            plugin_files = response[1]
            print("LOG: Able to find plugin files section in plugin developer agent response.")
        except IndexError:
            plugin_files = response[0]
            print("LOG: Could not find plugin files section in plugin developer agent response.")

        # Try to extract JSON from the section
        try:
            json_start = plugin_files.index("```json") + len("```json")
            json_end = plugin_files.index("```", json_start)
            plugin_files = plugin_files[json_start:json_end].strip()
            plugin_files = json.loads(plugin_files) 
            print("LOG: Successfully extracted JSON from plugin developer agent response.")
        # except various exceptions
        except (ValueError, json.JSONDecodeError, IndexError):
            print("LOG: Failed to extract JSON from plugin developer agent response.")
            return {"success": False, "error": "Invalid response format"}
        
        return {
            "success": True,
            "files": plugin_files
        }