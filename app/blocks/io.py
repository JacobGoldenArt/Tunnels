from dataclasses import dataclass
from blocks.base import Block
from typing import List, Dict, Any

@dataclass
class Entry(Block):
    """Entry node class to feed the text into the tunnel"""
    async def process(self, data: Dict):
        return {'block_input': data['block_input']}  # Inherit the input explicitly

@dataclass
class Exit(Block):
    """Exit node class to feed the text into the tunnel"""
    async def process(self, data: Dict):
        return {'block_output': data['output']}  # Use 'output' as in `TextGenerator` process
