

'''
Rough notes - Flow Plan
- Assume the frontend is a chat UI, with an initial greeting and asking user to begin by telling a bit about the plugin they want to create.
- The user provides a generic brief response of what they want.
- The wordpress consultant agent is invoked, it will ask the fixed questions that it needs.
- After the user answers all questions, the plugin information is finalized and WordpressDeveloperAgent is invoked.
- The developer agent will generate the plugin code based on the information provided by the consultant agent.

The code begins with assumption that response to first user message is recieved.
Frontend backend parts are denoted by --<part>-- comments.
'''

import os
from wordpress_consultant import WordPressConsultantAgent
from wordpress_developer import WordPressDeveloperAgent

def main():
    consultant_agent = WordPressConsultantAgent()
    developer_agent = WordPressDeveloperAgent()

    # --Frontend--
    print("AI: Hello! I am your WordPress plugin consultant. To create a plugin, I will need to ask you a few questions to understand your requirements better.")

    # --Backend--
    # Begin the consultation process (chat loop)
    consultant_response: dict = consultant_agent.consult()
    while not consultant_response.get("finalized", False):
        
        # --Frontend--
        # Show AI message, get user input
        print(f"AI: {consultant_response.get('message', '')}")
        user_input = input("User: ")
        print()

        # --Backend--
        consultant_response = consultant_agent.consult(user_input)
    
    # --Frontend--
    # Final message shown before invoking developer agent
    print(f"AI: {consultant_response.get('message', '')}")

    # --Backend--
    # Invoke the developer agent with the finalized plugin information
    plugin_info = consultant_agent.get_plugin_info()
    developer_response: dict = developer_agent.generate_plugin_code(plugin_info)
    
    if not developer_response.get("success", False):

        # --Frontend--
        print("AI: There was an error generating the plugin code. Please try again later.")
        exit(1)

    # --Backend--
    # Begin saving generated code files locally, and zipping them
    plugin_name = developer_response.get("plugin_name", "plugin")
    generated_files = developer_response.get("files", {})
    php_code = generated_files.get("plugin.php", "")
    js_code = generated_files.get("script.js", "")
    css_code = generated_files.get("style.css", "")

    # save to local
    # create `plugin_name` directory if not exists
    os.makedirs(plugin_name, exist_ok=True)
    
    # save php code to `plugin_name/plugin_name.php`
    with open(os.path.join(plugin_name, f"{plugin_name}.php"), "w") as f:
        f.write(php_code)
    # save js code to `plugin_name/assets/js/script.js`
    os.makedirs(os.path.join(plugin_name, "assets", "js"), exist_ok=True)
    with open(os.path.join(plugin_name, "assets", "js", "script.js"), "w") as f:
        f.write(js_code)
    # save css code to `plugin_name/assets/css/style.css`
    os.makedirs(os.path.join(plugin_name, "assets", "css"), exist_ok=True)
    with open(os.path.join(plugin_name, "assets", "css", "style.css"), "w") as f:
        f.write(css_code)

    # --Frontend--
    print(f"AI: The plugin code has been generated successfully! You can find it in the '{plugin_name}' directory.")
    # Actually will be a downloadable zip file in the real implementation

