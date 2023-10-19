import unittest
from tunnel.base import Tunnel
from typing import List
from blocks.base import Block
from blocks.io import Entry, Exit
from blocks.text import TextGenerator, Summarizer, Translator

def createNewTunnel(name: str) -> Tunnel:
    return Tunnel(name)

def editTunnel(tunnel: Tunnel, new_name: str) -> None:
    tunnel.name = new_name

def deleteTunnel(tunnel: Tunnel) -> None:
    del tunnel

def createNewBlock(type: str, name: str, sys: str) -> Block:
    if type == "summarize":
        return Summarizer(name=name, system_prompt=sys, temperature=0.5, max_tokens=300)
    # Add other block types as needed

def editBlock(block: Block, new_name: str = None, new_sys: str = None) -> None:
    if new_name:
        block.name = new_name
    if new_sys:
        block.system_prompt = new_sys

def deleteBlock(block: Block) -> None:
    del block

def addBlockToTunnel(tunnel: Tunnel, block: Block) -> None:
    tunnel.add_block(block)

def addTarget(block: Block, targets: List[str]) -> None:
    for target in targets:
        block.add_target(target)