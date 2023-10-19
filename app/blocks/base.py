import asyncio
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union

@dataclass
class Block:
    """
    The Block class is the base for various processing units within the pipeline.
    Each Block receives data, performs processing and passes forward the processed data.
    """
    name: str  # unique name of the block
    targets: List[str] = field(default_factory=list)  # list of blocks where this block passes its processed data
    data: Optional[Dict[str, Any]] = field(default_factory=dict)  # stores the data processed by this block

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Placeholder for the processing function.
        This function is meant to be overridden by derived classes to provide actual data processing.
        By default, this function acts as an identity function.
        """
        return data

    async def run(self, data: Dict[str, Any], blocks: Dict[str, 'Block']) -> None:
        """
        Executes the process function and runs the next blocks in the pipeline.
        data: input data for this block.
        blocks: dictionary of all blocks in the pipeline for access to the next block instances.
        """
        self.data = await self.process(data)
        print(f'Data processed by {self.name}: {self.data}')
        await asyncio.gather(*(blocks[target].run(self.data, blocks) for target in self.targets))

    def add_target(self, target: Union[str, List[str]]) -> None:
        """
        Adds blocks names in the 'targets' list where this block will pass its processed data.
        Supports addition of single or multiple target blocks at a time.
        """
        if isinstance(target, list):
            self.targets.extend(target)
        else:
            self.targets.append(target)
