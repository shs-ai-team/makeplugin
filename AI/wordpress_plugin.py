from enum import Enum


class WordPressPluginCategory(Enum):
    WIDGET = "widget"
    FORM = "form"
    BUTTON = "button"
    SHORTCODE = "shortcode"

    @classmethod
    def get_categories(cls):
        return [category.value for category in cls]
    


class WordpressPlugin:
    '''
    Represents a WordPress plugin and its attributes.
    '''
    def __init__(self, name: str= None, description: str=None, category: WordPressPluginCategory=None, author: str=None, other_info: dict=None):
        self.plugin_name = name
        self.plugin_description = description
        self.category = category
        self.author = author
        self.other_info = other_info if other_info is not None else {}
    
    def get_fields_info(self):
        '''
        Returns a dictionary of fields and short information about them.
        '''
        return {
            "plugin_name": "string - Name of the plugin.",
            "plugin_description": "string - Short description of the plugin.",
            "category": f"string - Category of the plugin (Allowed values: {', '.join([cat.value for cat in WordPressPluginCategory])}).",
            "author": "string - Author name.",
            "other_info": "dict - Additional information about the plugin."
        }
    
    def get_plugin_info(self):
        '''
        Returns a dictionary containing the plugin's information.
        '''
        return {
            "plugin_name": self.plugin_name,
            "plugin_description": self.plugin_description,
            "category": self.category,
            "author": self.author,
            "other_info": self.other_info
        }