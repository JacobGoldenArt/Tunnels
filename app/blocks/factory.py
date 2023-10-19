from kit.io import IO
from kit.word_transformers import Summarizer, Translator, TextGenerator
from llms.openai.openai_chat import ChatBot
from uuid import uuid4
from typing import Dict, List, Optional
from loguru import logger

class BlockFactory:
    """This class will handle the creation of blocks
    The user will choose a block type, give it a name, and provide one or more target blocks, and the block will be created
    """
    name: str
    id = uuid4() # generate a unique id for the node
    block_type: str # the type of block to be created e.g. ChatBot, Summarizer, Translator, TextGenerator
    source_blocks: list # 1 or more source blocks

    type_map = {
        'ChatBot': ChatBot,
        'Summarizer': Summarizer,
        'Translator': Translator,
        'TextGenerator': TextGenerator
        # add other classes here...
    }

    @classmethod
    def create(cls, name,block_type,source_blocks):
        """This function will handle the creation of blocks"""
        cls.name = name
        b_type = cls.type_map.get(block_type)
        source_blocks = cls.source_blocks
        # create a new instance of b_type
