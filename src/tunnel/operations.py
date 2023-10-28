from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from .base import Tunnel, Block
from blocks.test_block import TestBlock
from tunnel.routing import Routing
from db.dao import TunnelDAO, BlockDAO
from loguru import logger


@dataclass
class TunnelOps:
    """
    Handles operations on tunnels.
    """

    tunnel_dao: TunnelDAO
    block_dao: BlockDAO
    running_tunnels: Dict[str, Any] = field(default_factory=dict)

    def newTunnel(self, name: str) -> str:
        """
        Create a new tunnel.
        """
        tunnel_new = Tunnel(name=name, blocks={}, routing=Routing(), tunnel_output={})
        tunnel_id = self.tunnel_dao.save(tunnel_new)
        logger.success(f"Tunnel {tunnel_id} was created")
        return tunnel_id

    def editTunnel(self, tunnel_id: int, new_name: str) -> None:
        """
        Edit the name of a tunnel.
        """
        tunnel = self.tunnel_dao.get(tunnel_id)
        if tunnel is not None:
            tunnel.name = new_name
            self.tunnel_dao.update(tunnel_id, tunnel)  # Use update method here
            logger.success(f"Tunnel {tunnel_id} renamed to {new_name}")
        else:
            logger.error(f"No tunnel found with id {tunnel_id}")

    def getTunnel(self, tunnel_id: int) -> Optional[Tunnel]:
        """
        Get a tunnel by its id.
        """
        tunnel_data = self.tunnel_dao.get(tunnel_id)
        if not tunnel_data:
            logger.error(f"No tunnel found with id {tunnel_id}")
            return None
                # Create a Tunnel object
        tunnel_obj = Tunnel(name=tunnel_data.name)

        # Create Block objects for each block in the tunnel
        for block_data in tunnel_data.blocks.values():
            block_obj = self.block_factory(block_data)
            tunnel_obj.add_block(block_obj)

        return tunnel_obj
        
    def addBlockToTunnel(self, tunnel_id: int, block_id: int) -> None:
        """
        Add a block to a tunnel.
        """
        tunnel = self.tunnel_dao.get(tunnel_id)
        block = self.block_dao.get(block_id)
        if tunnel is not None and block is not None:
            tunnel.add_block(block)
            self.tunnel_dao.update(tunnel_id, tunnel)
            logger.success(f"Block {block_id} added to Tunnel {tunnel_id}")
        else:
            logger.error(f"Could not find Tunnel {tunnel_id} or Block {block_id}")


    def deleteTunnel(self, tunnel_id: int) -> None:
        """
        Delete a tunnel by its id.
        """
        self.tunnel_dao.delete(tunnel_id)
        logger.success(f"Tunnel {tunnel_id} was deleted")

    def block_factory(self, block_data: Dict[str, Any]) -> Block:
        """
        Factory method for creating blocks.
        """
        block_type = block_data.type
        block_name = block_data.name
        block_data = block_data.data

        if block_type == "TestBlock":
            return TestBlock(name=block_name, data=block_data)

    async def runTunnel(self, tunnel_id: int, data: str) -> None:
        """
        Run a tunnel with the given data.
        """
        tunnel_data = self.tunnel_dao.get(tunnel_id)

        if not tunnel_data:
            logger.error(f"No tunnel found with id {tunnel_id}")
            return

        tunnel_obj = Tunnel(name=tunnel_data.name, routing=tunnel_data.routing)  # Include routing when creating the Tunnel object
        for block_data in tunnel_data.blocks.values():
            block_obj = self.block_factory(block_data)
            tunnel_obj.add_block(block_obj)

        # Add the routes between the blocks
        for source_block_name, target_block_name in tunnel_data.routing.routes.items():
            tunnel_obj.connect_blocks(source_block_name, target_block_name)

        tunnel_out = await tunnel_obj.run(data)
        tunnel_data.tunnel_output = tunnel_out

        self.tunnel_dao.update(tunnel_id, tunnel_data)
