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

    async def process(self, data: Dict[str, Any]) -> None:
        self.tunnel_input = data
        for block in self.blocks.values():
            await block.process()
        return self.tunnel_output