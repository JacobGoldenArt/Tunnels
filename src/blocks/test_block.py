from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from loguru import logger
from blocks.block_base import Block


@dataclass
class TestProcess:
    """
    This is a test process to test block functionality.
    """

    async def test_process(self, data: str) -> str:
        """
        Process the data and return the processed data.
        """
        return f"Processed {data}"


class TestBlock(Block):
    """
    This is a block in its simplest form to test block functionality.
    """

    type: Optional[str] = field(default=None)

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the data and return the processed data.
        """
        data_input: str = data.get(self.name, "")
        process_data = TestProcess()
        generated_text = await process_data.test_process(data_input)
        logger.info(f"{self.name} generated the following text: {generated_text}")
        return {self.name: generated_text}
