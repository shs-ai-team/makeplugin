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

        self.requirements_responses = {step_name: None for step_name in self.requirements_steps_names[:-1]}

    def get_plugin_info(self):
        '''
        Returns the plugin information gathered so far.
        '''
        info = self.wordpress_plugin.get_plugin_info()
        return {k: v for k, v in info.items() if v is not None}
    
    def consult(self, user_input: str=None) -> dict:
        '''
        Takes response to previous question, and returns the next question to ask.
        Expects no input on the first call.
        ''' 

        current_step = self.requirements_steps_names[self.requirements_steps_completed]

        # store user response to previous question
        if self.requirements_steps_completed > 0:  # no response when first called
            self.requirements_responses[current_step - 1] = user_input  
        
        next_requirement_message = self.requirements_messages[current_step]

        if current_step == "other_info":
            plugin_info = self.get_plugin_info()
            next_requirement_message = next_requirement_message.format(plugin_info=plugin_info)

        self.requirements_steps_completed += 1

        if finalized := (self.current_step == "final"):
            




        