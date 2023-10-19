from rich.markdown import Markdown
from rich import print as rprint
from openai_api.openai_chat import OpenaiChatCompletion
import dotenv

dotenv.load_dotenv()

# Usage with verbose mode on, "obj" for object or "thread" for full thread
my_chat = OpenaiChatCompletion(
    sys="You are a helpful assistant.",
    verbose="user_input",
    temperature=0.6,
    max_tokens=30,
)

while True:
    user_input = input("Write message here: ")
    chat_response = my_chat(user_input)
    rprint("[bold cyan]DarkMatterBot:[/bold cyan]")
    rprint(Markdown(chat_response))
