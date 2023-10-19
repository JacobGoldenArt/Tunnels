from tunnel.base import Tunnel
from blocks.io import Entry, Exit
from blocks.text import Summarizer, Translator
from data.examples import longTextExample
import asyncio

myTunnel = Tunnel("myTunnel")

shortSummary = Summarizer(
      name="shortSummary",
      system_prompt="Create a short summary of the following text. No more then 100 words",
      temperature=0.5,
      max_tokens=200
)
technicalSummary = Summarizer(
      name="technicalSummary",
      system_prompt="Create a 500 word summary of the following text. The audience is technical, so please include the appropriatte level of details. Be sure to include some bullet points of the key take-aways.",
      temperature=0.5,
      max_tokens=300
)
easyReadSummary = Summarizer(
      name="easyReadSummary",
      system_prompt="Create a 300 word summary of the following text. Make sure the summary is easy to read and understand for a general public audience. Be sure to include some bullet points of the key take-aways.",
      temperature=0.8,
      max_tokens=300
)
entryBlock = Entry(
    name="entryBlock",
)
exitBlock = Exit(
    name="exitBlock",
)

myTunnel.add_block(entryBlock)
myTunnel.add_block(exitBlock)
myTunnel.add_block(shortSummary)
myTunnel.add_block(technicalSummary)
myTunnel.add_block(easyReadSummary)

# Connect source block to target blocks
myTunnel.blocks['entryBlock'].add_target(['technicalSummary', 'easyReadSummary'])
myTunnel.blocks['technicalSummary'].add_target(['shortSummary', 'exitBlock'])
myTunnel.blocks['easyReadSummary'].add_target('shortSummary')
myTunnel.blocks['shortSummary'].add_target('exitBlock')

# Set entry and exit blocks
myTunnel.set_entry('entryBlock')
myTunnel.add_exit('exitBlock')

asyncio.run(myTunnel.run({"block_input": longTextExample}))
