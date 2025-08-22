import os
import json
import uuid
import zipfile


class Session:
    SESSIONS_DIR = "sessions"  # folder to store session JSON files

    def __init__(self, session_id=None):

        os.makedirs(self.SESSIONS_DIR, exist_ok=True)

        # create new session if no ID provided
        if not session_id:
            self._create_new_session()
            return

        # Try to load existing session
        self.session_folder = os.path.join(self.SESSIONS_DIR, session_id)
        session_messages_path = os.path.join(self.session_folder, "messages.json")

        if not os.path.exists(session_messages_path):
            # Session file doesn't exist, create new
            self._create_new_session()
            return
        
        # Load existing session data
        with open(session_messages_path, "r") as f:
            data = json.load(f)

            self.id_ = session_id
            self.messages = data.get("messages")

    def _create_new_session(self):
        self.id_ = str(uuid.uuid4())
        self.session_folder = os.path.join(self.SESSIONS_DIR, self.id_)
        os.makedirs(self.session_folder, exist_ok=True)
        self.messages = [
            {"role": "consultant", "content": "Hi, I am Plugin Pal - your WordPress plugin assistant!\n To begin, please describe the plugin you want to create."}
        ]
        self.save_messages()


    def save_messages(self):
        session_messages_path = os.path.join(self.session_folder, "messages.json")
        with open(session_messages_path, "w") as f:
            json.dump({
                "messages": self.messages,
            }, f, indent=2)


    def add_message(self, role, content, **kwargs):
        message = {"role": role, "content": content}
        message.update(kwargs)
        self.messages.append(message)
        
        self.save_messages()


    def get_messages(self):
        return self.messages
    
    @staticmethod
    def save_plugin_files_zip(session_folder, plugin_files: dict):
        
        # determine next generation index
        existing_zips = [f for f in os.listdir(session_folder) if f.startswith("generation_") and f.endswith(".zip")]
        if not existing_zips:
            generation_id = 0
        else:
            indices = [int(f.split("_")[1].split(".")[0]) for f in existing_zips]
            generation_id = max(indices) + 1

        # create zip and write files
        zip_path = os.path.join(session_folder, f"generation_{generation_id}.zip")
        with zipfile.ZipFile(zip_path, "w") as zf:
            for relative_path, content in plugin_files.items():
                zf.writestr(relative_path, content)

        return generation_id

    def add_development_result(self, plugin_files: dict, usage_instructions: str=None):

        if plugin_files == {}:
            # Add (failiure) developer role message
            self.add_message(
                role="developer",
                content="Sorry I was unable to create the files, please try again.",
                zip_id=-1,
            )
        else:
            # Save plugin files as zip to session folder
            generation_id = self.save_plugin_files_zip(self.session_folder, plugin_files)

            # Add developer role message
            dev_message = f"I've created your plugin, packaged as a zip, ready to download and install!. Here are some instructions on how to get started with it:\n{usage_instructions}"
            self.add_message(
                role="developer",
                content=dev_message,
                zip_id=generation_id,
            )

    @classmethod
    def get_all_sessions(cls):
        sessions = []
        if not os.path.exists(cls.SESSIONS_DIR):
            return sessions

        for session_id in os.listdir(cls.SESSIONS_DIR):
            session_folder = os.path.join(cls.SESSIONS_DIR, session_id)
            messages_path = os.path.join(session_folder, "messages.json")
            session_data = {"id": session_id, "messages": []}
            if os.path.exists(messages_path):
                try:
                    with open(messages_path, "r") as f:
                        data = json.load(f)
                        session_data["messages"] = data.get("messages", [])
                except Exception:
                    pass
            sessions.append(session_data)

        return sessions





