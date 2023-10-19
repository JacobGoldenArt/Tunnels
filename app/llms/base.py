import openai
from dataclasses import dataclass
from dotenv import load_dotenv
from loguru import logger
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class LLM():
        """"This is the base class for all OpenAI endpoints."""
        prompt: str
        system_prompt: str

        def chat(self, temperature: float, max_tokens: int):
            """This method is used to generate chat completions from an OpenAI model."""
            system_prompt = self.system_prompt

            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                      "role": "system",
                      "content": system_prompt
                    },
                    {
                      "role": "user",
                      "content": self.prompt
                    }
                  ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            ai_response = reply['choices'][0]["message"]["content"]
            return ai_response

        def instruct(self, temperature: float, max_tokens: int):
            """This method is used to generate instruct completions from an OpenAI model."""
            prompt =  self.prompt + "\n" + self.system_prompt

            reply = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            ai_response = reply['choices'][0]['text']
            return ai_response
