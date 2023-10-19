import datetime
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv

# Load the .env file
dotenv.load_dotenv()

uri = os.environ.get("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.ghost_db
chat_history_db = db.chat_history

#get the current data and time
now = datetime.datetime.now()

# mongoDB adds the _id field automatically, so we don't need to add it
# I will need to fomat the chatbot thread data to match the format of the chat_history_text_example
chat_history_text_example = [
    {
        'time_stamp': now,
        'turns': [
            {'USER': "Hi, How are you today! I'm Jacob, what's your name?", 'ASSISTANT': "Hello! My name is Samantha, and I'm delighted to meet you."},

            {'USER': 'Hi Samantha, Can you tell me how as an AI you perceive the world?', 'ASSISTANT': "Hello! While I don't perceive the world in the same way a human does..."}

        ]
    }
]

result = chat_history_db.insert_many(chat_history)
document_ids = result.inserted_ids

print("# of chats inserted " + str(len(document_ids)))
print(f"_ids of inserted chats {document_ids}")

client.close()
