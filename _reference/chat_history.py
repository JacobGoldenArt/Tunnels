import os
import datetime
from typing import Optional, Dict, List
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from info.feedback import Feedback
import dotenv

dotenv.load_dotenv()

uri = os.environ.get("MONGO_URI")

print("uri: ", uri)

class History:
    """A class for maintaining and storing the history of a conversation."""

    def __init__(self, sys: str, verbose: Optional[str] = None) -> None:
        """
        Initialize a conversation with a system message and setup connection to MongoDB.
        sys: str : The initial system message.
        """
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = self.client.ghost_db.chat_history
        self.history = [{"role": "system", "content": sys}]
        self.verbose = verbose

        # Create a session at startup and save it to get session_id
        session_data = {"turns": self.history, "time_stamp": datetime.datetime.now()}
        session_id = self.db.insert_one(session_data).inserted_id
        self.session_id = session_id  # keeping track of session ID

        # Ping the MongoDB to check if connected
        try:
            self.client.admin.command("ping")
            Feedback.generate_feedback(
                "Pinged your deployment. You successfully connected to MongoDB!"
            )
        except Exception as e:
            Feedback.register_error(
                e,
                msg="Connection to MongoDB failed!",
            )

    def add(self, role: str, content: str):
        """
        Append a new role-content pair to the chatbot history and update the database.
        role : str : The role related to this content, either 'user' or 'assistant'.
        content : str : The content for this role.
        """
        self.history.append({"role": role, "content": content})
        self.save_to_db()
        Feedback.generate_feedback("Chat added to the db")

    def save_to_db(self):
        """
        Update the existing document in the MongoDB with the modified chat history.
        """
        self.db.update_one({"_id": self.session_id}, {"$set": {"turns": self.history}})

    def load_from_db(self, session_id: str) -> None:
        # Load a session based on session_id

        # Clear current history first - as we would be loading a previous session
        self.history = []

        # MongoDB find_one returns None if the document does not exist
        session_data = self.db.find_one({"_id": ObjectId(session_id)})
        if session_data:
            self.history = session_data.get("turns", [])
            # Set the current session_id to the loaded session's ID
            self.session_id = session_id
        else:
            print(f"No session found with provided id: {session_id}")

    def get_last(self, n: int) -> List[Dict[str, str]]:
        return self.history[-n:]

    def get_full_history(self) -> List[Dict[str, str]]:
        return self.history

    def __del__(self):
        # Close the client connection when the instance is deleted
        self.client.close()
