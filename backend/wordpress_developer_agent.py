import json
from .ai import AI
from .prompts import wordpress_developer_agent_system_prompt, wordpress_developer_agent_user_prompt_template
from .session import Session
from .models import UserMessage
from .wordpress_consultant_agent import WordPressConsultantAgent


class WordpressDeveloperAgent:
    """
    Developer Agent responsible for generating WordPress plugin code
    based on finalized requirements from the Consultant Agent.

    Context order:
    - System role
    - If a past development exists:
        - consultant requirements JSON that led to that dev (as user message)
        - dev's output itself
        - user free-form messages after that dev (merged as one, to show requested changes)
    - Latest finalized consultant requirements JSON
    """


    @staticmethod
    def build_context(session: Session) -> list[dict]:
        """
        Build context for the developer agent.

        If no developer message is found in history, returns [].

        If a developer message is found, returns a slice of history that contains:
            - Consultant JSON from the development just before the last developer message
            - That last developer message (its raw response)
            - All user free-text messages since then, combined into one
        """
        context = []
        session_messages = session.get_messages()

        # Search latest `developer` role message and add it to `context` if found
        i = len(session_messages) - 1
        while i > 0:
            message = session_messages[i]
            if message["role"] == "developer":
                message["content"] = message["raw_response"]
                context.append(message)
                break
            i -= 1

        # no past dev messages found -> return empty context
        else:
            return context

        # Add the requirements from `consultant` message just before latest `developer` message as a `user` message
        previous_requirements_message = session_messages[i - 1]
        previous_requirements_message["role"] = "user"
        formatted_requirements = json.dumps(
            {"requirements": previous_requirements_message["requirements"]},
            indent=2
        )
        previous_requirements_message["content"] = f"# Plugin Requirements:\n``json\n{formatted_requirements}\n```"
        context.insert(0, previous_requirements_message) 
        
        # Add content of all `user` role messages after latest `developer` role message to `context` as a single message
        changes_message = "# Changes Requested To Previous Development:"
        while i < len(session_messages):
            message = session_messages[i]
            if message["role"] == "user":
                changes_message += f"\n{message['content']}"
            i += 1
        context.append(UserMessage(content=changes_message).model_dump())

        return context

    @staticmethod
    def generate_plugin_files(requirements: dict, session: Session):
        """
        Generate plugin files from the latest finalized requirements.
        """

        # form developer agent user prompt using
        wp_dev_agent_user_message = wordpress_developer_agent_user_prompt_template.substitute(
            plugin_requirements=requirements
        )

        # Gather past context
        dev_context = WordpressDeveloperAgent.build_context(session)
        
        # form messages for AI call
        messages = [
            {"role": "system", "content": wordpress_developer_agent_system_prompt},
            *dev_context,
            {"role": "user", "content": wp_dev_agent_user_message}
        ]

        ai_response = AI.get_response(messages)

        # Parse response

        # Find the '## Plugin Files' section
        response_parts = ai_response.strip().split("## Plugin Files")
        try:
            plugin_files = response_parts[1]
            print("LOG: Successfully able to find plugin files section in plugin developer agent response.")
        except IndexError:
            plugin_files = response_parts[0]
            print("LOG: Could not find plugin files section in plugin developer agent response.")

        # Try to extract JSON from the section
        try:
            if "```json" in plugin_files:
                json_start = plugin_files.index("```json") + len("```json")
            else:
                json_start = plugin_files.index("```") + len("```")
            json_end = plugin_files.index("```", json_start)
            plugin_files = plugin_files[json_start:json_end].strip()
            plugin_files = json.loads(plugin_files) 
            print("LOG: Successfully extracted JSON from plugin developer agent response.")
        except (ValueError, json.JSONDecodeError, IndexError):
            print("LOG: Failed to extract JSON from plugin developer agent response.")
            plugin_files = {}

        usage_instructions = WordPressConsultantAgent.get_usage_instructions(plugin_files) if plugin_files else ""
        
        session.add_development_result(
            plugin_files=plugin_files,
            usage_instructions=usage_instructions,
            raw_response=ai_response
        )

