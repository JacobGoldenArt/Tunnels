import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
from bson.objectid import ObjectId
import pprint

# Load the .env file
dotenv.load_dotenv()

uri = os.environ.get("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.ghost_db

chat_history = db.chat_history

session_id_to_query = '650a02b4d99a4c2de04c0da0'
n_last_turns = 5  # Number of turns you want to retrieve

session_data = chat_history.find_one({'_id': ObjectId(session_id_to_query)})  # Changed 'session_id' to '_id' and added ObjectId conversion

last_n_turns = []  # Initialize to an empty list

if session_data:
    last_n_turns = session_data.get('turns', [])[-n_last_turns:]  # Using .get() to safely fetch 'turns'

# Redefining the function to print turns, in case you want to run it in your local terminal.
def print_turns(turns):
    for i, turn in enumerate(turns):
        user_text = turn.get('USER', 'No user text')
        assistant_text = turn.get('ASSISTANT', 'No assistant text')
        print(f"Turn {i+1}:\nUser: {user_text}\nAssistant: {assistant_text}\n---")


# Demonstrate the function
print_turns(last_n_turns)


client.close()
