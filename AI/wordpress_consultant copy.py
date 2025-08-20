from ai import AI
from wordpress_plugin import WordpressPlugin, WordPressPluginCategory

class WordPressConsultantAgent:
    '''
    Represents the chat agent acting as a WordPress consultant to
    gather and understand user requirements and prepare for 
    generation.
    Requirements gathering steps:
    1. Ask what the plugin is about.
    2. Ask for the plugin name.
    3. Infer the plugin category.
    4. Confirm category from user, giving other options as well
    5. Ask for the author name.
    7. Show structured understood information, so far.
    8. Ask for any additional information.
    9. Finalize the plugin information and return it. (Generation done by another agent)
    '''
    def __init__(self):
        self.wordpress_plugin = WordpressPlugin()

        self.system_prompt = """## Role:
        You an expert and experienced Wordpress consultant, with strong understanding and familiarity with Wordpress plugin development, working for a top wordpress development agency.
        
        ## Task:
        You task is to formalize and structure the requirements gathered at each step of consultation in a predecided fixed format, for easy understanding and further processing.

        ## Input:
        You will be given the the following information:
        - The requirement we are currently gathering.
        - The question we asked the client.
        - The client's response.

        ## Output:
        We need only a formal JSON-ified version of the requirement needed by us at the current stage.  The purpose of the format is to capture formally and consisely the requirement gathered in the current consultation step. 

        Response format:
        ```json
        {
            


        Details of format:
        
        
        self.requirements_messages = {
            "plugin_name": "To begin, could you please tell me a bit about the plugin you want to create?\nWhat exactly should the plugin be called (the plugin name)?",
            "plugin_description": "Please provide a short description of what the plugin does.",
            "category": f"What category does the plugin fall into? Please choose from one of the following:\n- {'\n- '.join(WordPressPluginCategory.get_categories())}",
            "author": "Okay and what should I note as the author name for this plugin?",
            "other_info": """Okay, so far I have understood the following information about your plugin, please tell if you need to add anything:\n{plugin_info}""",
            "final": "Okay I shall begin generating the plugin now, please stand by."
        }
        self.requirements_steps_names = [step_name for step_name in self.requirements_messages_dict.keys()]
        self.requirements_steps_completed = 0

    def get_plugin_info(self):
        '''
        Returns the plugin information gathered so far.
        '''
        info = self.wordpress_plugin.get_plugin_info()
        return {k: v for k, v in info.items() if v is not None}
    
    def consult(self, user_input: str) -> dict:
        '''
        Main method to begin the consultation process.
        Takes user input and returns a response dictionary.
        '''

        current_step = self.requirements_steps_names[self.requirements_steps_completed]
        requirements_message = self.requirements_messages[current_step]

        if current_step == "other_info":
            plugin_info = self.get_plugin_info()
            requirements_message = requirements_message.format(plugin_info=plugin_info)

        # Prepare messages for AI
        messages = [    
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": }
        ]
