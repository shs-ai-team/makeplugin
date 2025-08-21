import json
from ai import AI
from prompts import wordpress_consultant_agent_system_prompt
from models import SystemMessage, UserMessage, ConsultantMessage
from session import Session

class WordPressConsultantAgent:

    @staticmethod
    def consult(user_message: str, session: Session):
    # def consult(self, user_message):
        # self.messages.append({"role": "user", "content": user_message})
        
        # Add user message to session
        user_message = UserMessage(content=user_message)
        session.add_message(user_message.role, user_message.content)

        # Form messages for AI call
        messages = session.get_messages()
        # TODO: trim messages history 
        messages.insert(0, SystemMessage(content=wordpress_consultant_agent_system_prompt).model_dump())

        response = AI.get_response(messages)

        # Strip the response of any extra formatting and parse it as JSON
        response_json = response.strip().split("```json")[-1].split("```")[0].strip()
        try:
            response_json = json.loads(response_json)
        except json.JSONDecodeError:
            response_json = {
                "requirements_finalized": False,
                "requirements": {},
                "response_to_user": "There was an error processing your request. Please try again."
            }
        
        # self.messages.append({"role": "consultant", "content": response})
        # Add new AI response to session
        session.add_message(ConsultantMessage(content=f"```json\n{json.dumps(response_json, indent=2)}```"))

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
        
