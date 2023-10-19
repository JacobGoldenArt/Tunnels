from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from blocks.base import Block

@dataclass
class Tunnel:
    """
    The Tunnel class organizes and maintains Blocks for data processing pipeline.
    The Tunnel controls how data is passed from block to block with asynchronous processing capabilities.
    """
    name: str  # unique name of the tunnel
    entry: Optional[str] = None  # name of the first block that begins processing
    exits: List[str] = field(default_factory=list)  # list of exit blocks that conclude processing
    blocks: Dict[str, Block] = field(default_factory=dict)  # stores all blocks to manage their instances

    def add_block(self, block: Block) -> None:
        """Adds a block into the tunnel's dictionary indexed by its unique name."""
        self.blocks[block.name] = block

    def set_entry(self, block: str) -> None:
        """Sets the initial block that starts the data processing pipeline within the tunnel."""
        self.entry = block

    def add_exit(self, block: str) -> None:
        """Adds a block into the list of final blocks that end the data processing pipeline within the tunnel."""
        self.exits.append(block)

    async def run(self, data: Dict[str, Any]) -> None:
        """
        Initiates the data processing pipeline within the tunnel.
        Data is passed forward starting from the 'entry' block.
        After all processing is concluded, data obtained at each 'exit' block is displayed.
        """
        if self.entry is None:
                raise ValueError("Entry block is not set in the tunnel.")

        await self.blocks[self.entry].run(data, self.blocks)
        for block_name in self.exits:
            print(f'Final data after {self.blocks[block_name].name}: {self.blocks[block_name].data}')
