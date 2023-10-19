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
chat_history = db.chat_history
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

for db in client.list_database_names():
    print(db)
