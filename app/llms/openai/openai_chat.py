from factory.block_base import Block
from dataclasses import dataclass
from loguru import logger
from llms.openai.openai_base import OpenAI
import asyncio


@dataclass
class ChatHistory:
    """
    A class for storing the chat history.
    """
    history = []

    def add(self, role, message):
        """
        Stores the chat message.

        :param role: a role (system, user, or assistant)
        :param message: a message text to be added to the history
        """
        self.history.append({"role": role, "message": message})

    def get_last(self, n):
        """
        Retrieves the last 'n' messages from the chat history.

        :param n: a number of messages to retrieve
        :return: a list of the last 'n' chat messages
        """
        return self.history[-n:]

    def get_all(self):
        """
        Retrieves all chat history.

        :return: a list of all chat messages
        """
        return self.history

@dataclass
class ChatBot(Block):
    """
    A ChatBot class for managing chat-based interactions.
    Inherits base functionality from the Node class.
    """
    system_prompt: str
    _chat_history = ChatHistory()

    async def process(self):
        """
        This method specifies how to process input data for the ChatBot class.
        """

        system_prompt = self.system_prompt
        prompt_input: str = self.data[self.source_block]

        # Getting the history of the last 5 messages
        ch = self._chat_history.get_last(n=5)

        # Combining the chat history with the input
        prompt =  str(ch) + "\n" + prompt_input
        openai_instance = OpenAI(prompt, system_prompt)

        # Generating the bot response and adding it to the chat history
        bot_response = openai_instance.chat()
        self._chat_history.add("assistant", bot_response)

        # Preparing output data
        self.data = {self.target_block: bot_response}
