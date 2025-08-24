import os
import json
import uuid
import zipfile
from copy import deepcopy
from models import ConsultantMessage



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
            ConsultantMessage(
                content="Hi, I am Plugin Pal - your WordPress plugin assistant!\n To begin, please describe the plugin you want to create.",
                requirements_finalized=False,
                requirements={}
            ).model_dump()
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
        return deepcopy(self.messages)
    
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

    def add_development_result(self, plugin_files: dict, usage_instructions: str, raw_response: str):

        if plugin_files == {}:
            # Add (failiure) developer role message
            self.add_message(
                role="developer",
                content="Sorry I was unable to create the files, please try again.",
                zip_id=-1,
                raw_response=raw_response
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
                raw_response=raw_response
            )

    @classmethod
    def get_all_session_ids(cls):
        """
        Returns a list of all session UUIDs.
        """
        session_ids = []
        if not os.path.exists(cls.SESSIONS_DIR):
            return session_ids

        for session_id in os.listdir(cls.SESSIONS_DIR):
            session_folder = os.path.join(cls.SESSIONS_DIR, session_id)
            if os.path.isdir(session_folder):
                session_ids.append(session_id)

        return session_ids

    @classmethod
    def get_all_session_data(cls):
        """
        Returns full session data including id and messages 
        """
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

    @classmethod
    def get_zip_path(cls, session_id, zip_id: int) -> str:
        """
        Returns the absolute path to the zip file for the given session and generation id.
        """
        session_folder = os.path.join(cls.SESSIONS_DIR, str(session_id))
        zip_filename = f"generation_{zip_id}.zip"
        zip_path = os.path.join(session_folder, zip_filename)
        return zip_path