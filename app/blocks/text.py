from .base import Block
from typing import Optional, Dict, Any
from llms.base import LLM
from dataclasses import dataclass, field

@dataclass
class TextGenerator(Block):
    """Parent Block class for text generation"""
    temperature: float = field(default=0.5)
    max_tokens: int = field(default=300)
    system_prompt: str = field(default="")

    async def process(self, data):
        """
        This method specifies how to process input data for the TextGenerator class.
        """
        # Gathering input data
        prompt_input: str = data['block_input']  # Change 'block_input' to the correct key
        system_prompt: str = self.system_prompt
        temperature: float = self.temperature

        llm_instance = LLM(prompt_input, system_prompt)

        # Generating the text
        generated_text = llm_instance.instruct(temperature, self.max_tokens)

        # Preparing output data
        data['output'] = generated_text  # Change 'self.target' to 'output'

        return data

@dataclass
class Translator(TextGenerator):
    """Child node class inherits from TextGenerator and generates a translation completion"""
    system_prompt: str = "Please translate the following text from English to French:"

@dataclass
class Summarizer(TextGenerator):
    """Child node class inherits from TextGenerator and generates a summarization completion"""
    system_prompt: str ="Please summarise the following text:"
