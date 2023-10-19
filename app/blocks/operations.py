import os
from .base import Block
from .text import TextGenerator, Translator, Summarizer
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
#block collection in db
blocks_c = app_db.blocks_c
#tunnels collection in db
tunnels_c = app_db.tunnels_c

block_types = {
    "textgen": "TextGenerator",
    "summ": "Summarizer",
    "transl": "Translator",
}

class BlocksOps(Block):
    def __init__(self, name):
        super().__init__(name)


    @classmethod
    def newBlock(cls, name, type: str = "textgen", tunnel_id: str = None):
        """Create a new block store it in the db and return its ID"""
        block_class = block_types[type]
        block_new = globals()[block_class](name)
        result = blocks_c.insert_one(block_new.__dict__)
        logger.success(f"{block_new} created")

        # Add the block to a tunnel that is stored in the database
        tunnel = tunnels_c.find_one({"_id": ObjectId(tunnel_id)})
        if tunnel is not None:
            tunnel['blocks'][str(result.inserted_id)] = block_new.__dict__
            tunnels_c.update_one({"_id": ObjectId(tunnel_id)}, {"$set": {"blocks": tunnel['blocks']}})
            logger.success(f"Block {block_new.name} added to Tunnel {tunnel['name']}")
        else:
            logger.error(f"No tunnel found with id {tunnel_id}")

        return str(result.inserted_id)

    @classmethod
    def editBlock(cls, block_id, updates):
        """Edit a block's parameters stored in the database"""
        result = blocks_c.update_one(
            {"_id": ObjectId(block_id)},
            {"$set": updates}
        )
        if result.modified_count == 0:
            logger.error(f"No block found with id {block_id}")
        else:
            logger.success(f"Block {block_id} updated")

            # Update the block in the tunnel
            tunnel = tunnels_c.find_one({"blocks." + block_id: {"$exists": True}})
            if tunnel is not None:
                for key, value in updates.items():
                    tunnel['blocks'][block_id][key] = value
                tunnels_c.update_one({"_id": ObjectId(tunnel['_id'])}, {"$set": {"blocks": tunnel['blocks']}})


    @classmethod
    def addTargets(cls, blk_id, targets: list):
        """Add targets to a block stored in the database"""
        result = blocks_c.update_one(
            {"_id": ObjectId(blk_id)},
            {"$push": {"targets": {"$each": targets}}}
        )
        if result.modified_count == 0:
            logger.error(f"No block found with id {blk_id}")
        else:
            logger.success(f"Block {blk_id} targets updated")

            # Update the block in the tunnel
            tunnel = tunnels_c.find_one({"blocks." + blk_id: {"$exists": True}})
            if tunnel is not None:
                tunnel['blocks'][blk_id]['targets'] = targets
                tunnels_c.update_one({"_id": ObjectId(tunnel['_id'])}, {"$set": {"blocks": tunnel['blocks']}})

    @classmethod
    def deleteBlock(cls, block_id) -> None:
        """Delete a block stored in the database"""
        result = blocks_c.delete_one({"_id": ObjectId(block_id)})
        if result.deleted_count == 0:
            logger.error(f"No block found with id {block_id}")
        else:
            logger.success(f"Block {block_id} was deleted")

            # Remove the block from the tunnel
            tunnel = tunnels_c.find_one({"blocks." + block_id: {"$exists": True}})
            if tunnel is not None:
                del tunnel['blocks'][block_id]
                tunnels_c.update_one({"_id": ObjectId(tunnel['_id'])}, {"$set": {"blocks": tunnel['blocks']}})