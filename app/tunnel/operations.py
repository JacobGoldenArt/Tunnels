import os
from .base import Tunnel
from loguru import logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import dotenv

# Load the .env file
dotenv.load_dotenv()

uri = os.environ.get("MONGO_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Create a new database and collection
app_db = client.app_db
tunnels_c = app_db.tunnels_c


class TunnelOps(Tunnel):
    def __init__(self, name):
        super().__init__(name)

    @classmethod
    def newTunnel(cls, name) -> str:
        """Create a new tunnel and return its ID"""
        tunnel_new = Tunnel(name)
        result = tunnels_c.insert_one(tunnel_new.__dict__)
        logger.success(f"{tunnel_new} created")
        return str(result.inserted_id)

    @classmethod
    def editTunnel(cls, tunnel_id, new_name):
        """Edit a tunnel's name"""
        result = tunnels_c.update_one(
            {"_id": ObjectId(tunnel_id)},
            {"$set": {"name": new_name}}
        )
        if result.modified_count == 0:
            logger.error(f"No tunnel found with id {tunnel_id}")
        else:
            logger.success(f"Tunnel {tunnel_id} renamed to {new_name}")

    @classmethod
    def deleteTunnel(cls, tunnel_id) -> None:
        """Delete a tunnel"""
        result = tunnels_c.delete_one({"_id": ObjectId(tunnel_id)})
        if result.deleted_count == 0:
            logger.error(f"No tunnel found with id {tunnel_id}")
        else:
            logger.success(f"Tunnel {tunnel_id} was deleted")