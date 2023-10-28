from dataclasses import dataclass
from typing import Optional, Union
from db.dao import BlockDAO
from tunnel.operations import TunnelOps
from blocks.base import Block
from loguru import logger


@dataclass
class BlockOps:
    """
    Handles operations on blocks.
    """

    block_dao: BlockDAO
    tunnel_ops: TunnelOps

    def newBlock(self, b: Block) -> int:
        """
        Create a new block.
        """
        block_id = self.block_dao.save(b)
        logger.success(f"New block {b.name} was created with id {block_id}")
        return block_id

    def retrieveBlock(self, block_id: int) -> Optional[Block]:
        """
        Retrieve a block by its id.
        """
        block_data = self.block_dao.get(block_id)
        if block_data is None:
            logger.error(f"No block found with id {block_id}")
            return None

        block_obj = self.tunnel_ops.block_factory(block_data)
        return block_obj

    def updateBlock(self, block_id: int, field: str, value: Union[str, int]) -> None:
        """
        Update a field of a block.
        """
        block_data = self.block_dao.get(block_id)
        if block_data:
            block_data[field] = value
            self.block_dao.save(block_data)
            logger.success(f"Block {block_id} updated with {field} = {value}")
        else:
            logger.error(f"No block found with id {block_id}")

    def deleteBlock(self, block_id: int) -> None:
        """
        Delete a block by its id.
        """
        self.block_dao.delete(block_id)
        logger.success(f"Block {block_id} was deleted")
