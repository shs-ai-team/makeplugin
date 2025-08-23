import json
from ai import AI
from prompts import (
    wordpress_consultant_agent_system_prompt,
    wordpress_plugin_usage_instructions_generator_system_prompt,
    wordpress_plugin_usage_instructions_generator_user_prompt_template
)
from models import SystemMessage, UserMessage, ConsultantMessage
from session import Session

class WordPressConsultantAgent:

    @staticmethod
    def consult(user_message: str, session: Session) -> ConsultantMessage:
        
        # Add user message to session
        user_message = UserMessage(content=user_message)
        session.add_message(user_message.role, user_message.content)

        # Form messages for AI call
        messages = session.get_messages()
        # TODO: trim messages history

        # modify `content` of each `consultant` message to packed expected output format for the AI call
        for message in messages:
            if message["role"] == "consultant":

                # pack
                _response_to_user = message["content"]
                _requirements = message["requirements"]
                _requirements_finalized = message["requirements_finalized"]
                _content_json = json.dumps({
                    "requirements_finalized": _requirements_finalized,
                    "requirements": _requirements,
                    "response_to_user": _response_to_user
                }, indent=2)

                message["content"] = f"```json\n{_content_json}\n```"
                
        messages.insert(0, SystemMessage(content=wordpress_consultant_agent_system_prompt).model_dump())

        response = AI.get_response(messages)

        # Strip the response of any extra formatting and parse it as JSON
        if "```json" in response:
            response_json = response.strip().split("```json")[-1].split("```")[0].strip()
        else:
            response_json = response.strip().split("```")[-1].split("```")[0].strip()

        try:
            response_json = json.loads(response_json)
        except json.JSONDecodeError:
            response_json = {
                "requirements_finalized": False,
                "requirements": {},
                "response_to_user": "There was an error processing your request. Please try again."
            }
        
        # Add new AI response to session
        new_ai_message = ConsultantMessage(
            content=response_json["response_to_user"],
            requirements_finalized=response_json["requirements_finalized"],
            requirements=response_json["requirements"]
        )
        session.add_message(
            role=new_ai_message.role,
            content=new_ai_message.content,
            requirements_finalized=new_ai_message.requirements_finalized,
            requirements=new_ai_message.requirements
        )

        return new_ai_message
    
    # def get_requirements(self):
    #     """
    #     Returns the current requirements as a JSON object.
    #     """
    #     last_response = self.messages[-1]["content"]
    #     try:
    #         response_json = json.loads(last_response.strip().split("```json")[-1].split("```")[0].strip())
    #         return response_json.get("requirements", {})
    #     except (json.JSONDecodeError, IndexError):
    #         return {}


    @staticmethod
    def get_usage_instructions(plugin_files: dict) -> str:
        # Prepare the messages for the AI call
        messages = [
            {"role": "system", "content": wordpress_plugin_usage_instructions_generator_system_prompt},
            {"role": "user", "content": wordpress_plugin_usage_instructions_generator_user_prompt_template.substitute(plugin_files=plugin_files)}
        ]

        # Call the AI to generate usage instructions
        usage_instructions = AI.get_response(messages=messages)
        
        # Parse and clean AI response
        instructions_heading_index = usage_instructions.find("# Instructions")
        if instructions_heading_index != -1:
            usage_instructions = usage_instructions[instructions_heading_index + len("# Instructions"):].strip()
        if usage_instructions.startswith("'''") and usage_instructions.endswith("'''"):
            usage_instructions = usage_instructions[3:-3].strip()

        # Return the generated usage instructions
        return usage_instructions
            

# if __name__ == "__main__":
    
#     with open("eg_plugin_response.txt", "r") as f:
#         response = f.read()

    
#     print("Extracting JSON")
#     response = response.strip().split("## Plugin Files")[1]
#     if "```json" in response:
#         response_json = response.strip().split("```json")[-1].split("```")[0].strip()
#     else:
#         response_json = response.strip().split("```")[-1].split("```")[0].strip()

#     print(response_json)
#     exit()
#     response_json = json.loads(response_json
#     print("Extracted. Calling AI")
#     print(response_json)

#     # usage_instructions = WordPressConsultantAgent.get_usage_instructions(response_json) 

#     # print("AI response recieved:\n\n")
#     # print(usage_instructions)