from tinydb import TinyDB, Query
from typing import Optional
from tunnel.base import Tunnel
from blocks.base import Block
from loguru import logger


class TunnelDAO:
    def __init__(self, db: TinyDB):
        self.db = db.table("tunnels")
        logger.info("Initialized TunnelDAO")

    def save(self, tunnel: Tunnel) -> int:
        tunnel_id = self.db.insert(tunnel.model_dump())
        logger.info(f"Saved tunnel with id {tunnel_id}")
        return tunnel_id

    def get(self, tunnel_id: int) -> Optional[Tunnel]:
        tunnel_data = self.db.get(doc_id=tunnel_id)
        if tunnel_data is not None:
            return Tunnel(**tunnel_data)
        else:
            logger.error(f"No tunnel found with id {tunnel_id}")
            return None

    def delete(self, tunnel_id: int) -> None:
        self.db.remove(doc_id=tunnel_id)
        logger.info(f"Deleted tunnel with id {tunnel_id}")

    def update(self, tunnel_id: int, tunnel: Tunnel) -> None:
            TunnelQuery = Query()
            self.db.update(tunnel.model_dump(), TunnelQuery.doc_id == tunnel_id)
            logger.info(f"Updated tunnel with id {tunnel_id}")


class BlockDAO:
    def __init__(self, db: TinyDB):
        self.db = db.table("blocks")
        logger.info("Initialized BlockDAO")

    def save(self, block: Block) -> int:
        block_id = self.db.insert(block.model_dump())
        logger.info(f"Saved block with id {block_id}")
        return block_id

    def get(self, block_id: int) -> Optional[Block]:
        block_data = self.db.get(doc_id=block_id)
        logger.info(f"Got block with id {block_id} {block_data}")

        if block_data is not None:
            return Block(**block_data)
        else:
            logger.error(f"No block found with id {block_id}")
            return None

    def delete(self, block_id: int) -> None:
        self.db.remove(doc_id=block_id)
        logger.info(f"Deleted block with id {block_id}")

    def update(self, block_id: int, block: Block) -> None:
        BlockQuery = Query()
        self.db.update(block.model_dump(), BlockQuery.doc_id == block_id)
        logger.info(f"Updated block with id {block_id}")
