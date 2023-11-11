from tinydb import TinyDB
from ops.block_ops import BlockOps
from ops.tunnel_ops import TunnelOps
from blocks.test_block import TestBlock
from db.dao import TunnelDAO, BlockDAO
from rich import print
import asyncio

import sys

from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", level="ERROR")

# Create and set up your data access objects (DAOs)
db = TinyDB("db.json")
tunnel_dao = TunnelDAO(db)
block_dao = BlockDAO(db)

# Instantiate BlockOps and TunnelOps
tunnel_ops = TunnelOps(tunnel_dao, block_dao)
block_ops = BlockOps(block_dao, tunnel_ops)


# Create a new tunnel
tunnel_id = tunnel_ops.newTunnel("WTF")
testBlock1 = {
    "type": "TestBlock",
    "name": "aBlock1",
}

testBlock2 = {
    "type": "TestBlock",
    "name": "bBlock2",
}

testBlock3 = {
    "type": "TestBlock",
    "name": "cBlock3",
}

# Create new blocks
testBlock1_id = block_ops.newBlock(TestBlock(**testBlock1))
testBlock2_id = block_ops.newBlock(TestBlock(**testBlock2))
testBlock3_id = block_ops.newBlock(TestBlock(**testBlock3))

# Retrieve blocks from the database
testBlock1 = block_ops.retrieveBlock(testBlock1_id)
testBlock2 = block_ops.retrieveBlock(testBlock2_id)
testBlock3 = block_ops.retrieveBlock(testBlock3_id)

# Get the tunnel object
tunnel = tunnel_ops.getTunnel(tunnel_id)

# Add blocks to the tunnel
tunnel_ops.addBlockToTunnel(tunnel_id, testBlock1_id)
tunnel_ops.addBlockToTunnel(tunnel_id, testBlock2_id)
tunnel_ops.addBlockToTunnel(tunnel_id, testBlock3_id)

# Make connections between blocks
tunnel.connect_blocks(testBlock1.name, testBlock2.name)
tunnel.connect_blocks(testBlock2.name, testBlock3.name)

# Save the tunnel to the database
# tunnel_ops.editTunnel(tunnel_id, tunnel.name)

# Create a new event loop
loop = asyncio.new_event_loop()

# Set the new event loop as the current event loop
asyncio.set_event_loop(loop)


async def main():
    # Use asyncio.ensure_future to run the coroutine
    # and return a Future representing the result of the function
    future = asyncio.ensure_future(
        tunnel_ops.runTunnel(tunnel_id, "Hello Test Blocks!")
    )

    # Await the Future to get the result of the function
    result = await future
    print(result)


# Run the main function until it completes
loop.run_until_complete(main())
