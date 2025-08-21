import json
from ai import AI
from prompts import wordpress_consultant_agent_system_prompt 

class WordPressConsultantAgent:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": wordpress_consultant_agent_system_prompt}
        ]

    def consult(self, user_message):
        self.messages.append({"role": "user", "content": user_message})
        
        response = AI.get_response(self.messages)

        # Strip the response of any extra formatting and parse it as JSON
        response_json = response.strip().split("```json")[-1].split("```")[0].strip()

        try:
            response_json = json.loads(response_json)
        except json.JSONDecodeError:
            return {
                "requirements_clarified": False,
                "requirements": {},
                "response_to_user": "There was an error processing your request. Please try again."
            }
        
        self.messages.append({"role": "consultant", "content": response})
        return response_json
    
    def get_requirements(self):
        """
        Returns the current requirements as a JSON object.
        """
        last_response = self.messages[-1]["content"]
        try:
            response_json = json.loads(last_response.strip().split("```json")[-1].split("```")[0].strip())
            return response_json.get("requirements", {})
        except (json.JSONDecodeError, IndexError):
            return {}
        
