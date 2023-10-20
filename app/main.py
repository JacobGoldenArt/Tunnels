from blocks.operations import BlocksOps
from tunnel.operations import TunnelOps
from data.examples import longTextExample
import asyncio

#Example of how to use the API to create a tunnel with 3 blocks
# and run it on a sample input

# Create a new tunnel
tunnel_id = TunnelOps.newTunnel("textTunnel")

shortSummary = {
      "name":"shortSummary",
      "system_prompt":"Create a short summary of the following text. No more then 100 words",
      "temperature":0.5,
      "max_tokens":200
}
technicalSummary = {
      "name":"technicalSummary",
      "system_prompt":"Create a 500 word summary of the following text. The audience is technical, so please include the appropriatte level of details. Be sure to include some bullet points of the key take-aways.",
      "temperature":0.5,
      "max_tokens":300
}

easyReadSummary = {
      "name":"easyReadSummary",
      "system_prompt":"Create a 300 word summary of the following text. Make sure the summary is easy to read and understand for a general public audience. Be sure to include some bullet points of the key take-aways.",
      "temperature":0.8,
      "max_tokens":300
}

# Create new blocks
shortSummary_id = BlocksOps.newBlock(tunnel_id,shortSummary)
technicalSummary_id = BlocksOps.newBlock(tunnel_id,technicalSummary)
easyReadSummary_id = BlocksOps.newBlock(tunnel_id,easyReadSummary)

# Connect source block to target blocks
BlocksOps.addTargets(technicalSummary_id, [easyReadSummary_id])
BlocksOps.addTargets(easyReadSummary_id, [shortSummary_id])
BlocksOps.addTargets(shortSummary_id, [])

# Run the tunnel
asyncio.run(TunnelOps.process(tunnel_id, {"block_input": longTextExample}))