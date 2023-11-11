from dataclasses import field
import asyncio
from pydantic import BaseModel
from typing import Dict, Any
from blocks.block_base import Block
from routes.routes import Routing
from loguru import logger


class Tunnel(BaseModel):
    """
    Represents a tunnel of blocks.
    """

    name: str
    blocks: Dict[str, Block] = field(default_factory=dict)
    routing: Routing = field(default_factory=Routing)
    tunnel_output: Dict[str, Any] = field(default_factory=dict)

    def add_block(self, block: Block) -> None:
        """
        Add a block to the tunnel.
        """
        self.blocks[block.name] = block
        return block

    def connect_blocks(self, source_block_name: str, target_block_name: str) -> None:
        """
        Connect two blocks in the tunnel.
        """
        if target_block_name not in self.blocks:
            self.routing.add_route(source_block_name, "tunnel_output")
        else:
            self.routing.remove_route(source_block_name, "tunnel_output")
            self.routing.add_route(source_block_name, target_block_name)

    def model_dump(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "blocks": {name: block.model_dump() for name, block in self.blocks.items()},
            "routing": self.routing.model_dump(),
            "tunnel_output": self.tunnel_output,
        }

    async def dispatch_to_targets(self, block_name: str) -> None:
        """
        Dispatch the output of a block to its targets.
        """
        block = self.blocks[block_name]
        await block.processed.wait()
        targets = self.routing.get_targets(block_name)
        for target_name in targets:
            if target_name == "tunnel_output":
                self.tunnel_output[block_name] = block.data
            else:
                target_block = self.blocks[target_name]
                await target_block.input(block.data)
        block.processed.clear()

    async def run(self, data: str) -> None:
        """
        Run the tunnel with the given data.
        """
        starters = set(self.blocks.keys()) - set(self.routing.routes.values())
        tasks = [self.blocks[block_name].input(data) for block_name in starters]
        tasks += [self.dispatch_to_targets(block_name) for block_name in starters]
        await asyncio.gather(*tasks)
