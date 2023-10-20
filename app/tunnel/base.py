from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from blocks.base import Block

@dataclass
class Tunnel:
    name: str
    blocks: Dict[str, Block] = field(default_factory=dict)
    tunnel_input: Dict[str, Any] = field(default_factory=dict)
    tunnel_output: Dict[str, Any] = field(default_factory=dict)

    def add_block(self, block: Block) -> None:
        self.blocks[block.name] = block

    async def process(self, data):
        processed_data = data
        for block_dict in self.blocks.values():
            # Convert the dictionary to a Block object
            block_obj = Block(**block_dict)
            # Process the data
            processed_data = await block_obj.process(processed_data)
        self.tunnel_output = processed_data