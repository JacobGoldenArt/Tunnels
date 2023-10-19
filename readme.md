 # Tunnels

 # README

 This repository provides an easy-to-use framework for creating asynchronous data processing pipelines with Python. Typical usage often involves text processing tasks (such as translation and summarization), but it can be extended to other forms of data processing tasks as well!

 ## Project Structure

 * `tunnel.py`: Contains the `Tunnel` class, which manages the entry and exit nodes along with handling the data flow between them.
 * `blocks` directory: Contains a variety of processing blocks, each with a specialized task.
     * `base.py`: Contains the base `Block` class that other specialized block classes inherit from.
     * `text.py`: Contains the `TextGenerator` class and text processing child classes 'Translator' and 'Summarizer'.
     * `io.py`: Contains the 'Entry' and 'Exit' block classes which act as input and output of the pipeline.
 * `llms` directory: Contains classes that interact with the OpenAI APIs.
     * `base.py`: Contains the `LLM` class, which acts as a base class for all OpenAI language model instructions and chat applications.

 ## Usage

 Here is an example of how to use the framework:

 ```python
 from tunnel.base import Tunnel
 from blocks.io import Entry, Exit
 from blocks.text import Summarizer, Translator
 import asyncio

 myTunnel = Tunnel("myTunnel")

 shortSummary = Summarizer(
     name="shortSummary",
     system_prompt="Create a short summary of the following text.",
     temperature=0.5,
     max_tokens=300
 )

 # ... (Define other blocks) ...

 entryBlock = Entry(name="entryBlock")
 exitBlock = Exit(name="exitBlock")

 myTunnel.add_block(entryBlock)
 myTunnel.add_block(exitBlock)
 myTunnel.add_block(shortSummary)

 # ... (Add other blocks) ...

 # Connect source block to target blocks
 myTunnel.blocks['entryBlock'].add_target(['shortSummary'])

 # ... (Connect other blocks) ...

 # Set entry and exit blocks
 myTunnel.set_entry('entryBlock')
 myTunnel.add_exit('exitBlock')

 asyncio.run(myTunnel.run({"block_input": myText}))
 ```

 In the above code, whenever we start processing, we give data as a dictionary to the entry block of the tunnel. The `Entry` block then processes the data, passing it to the rest of the blocks in the pipeline until it eventually reaches the exit block.

 ## Future Improvements

 While this pipeline framework serves its purpose, there are a few areas that could be improved upon in the future:

 1. **Error Handling**: Currently, there is minimal error handling in the event that something goes wrong during the processing. For example, if a certain block throws an exception, the pipeline stops. More robust error handling could go a long way towards making this system more resilient.

 2. **Parallel Processing**: Though Python is single-threaded, the async calls can be used for IO or external service tasks (network requests, file IO, etc.). Research on optimal use of parallel processing in this respect would be beneficial based on pipeline nature and processing blocks' characteristics.

 3. **Dynamic Pipeline Configuration**: Right now, the pipeline has to be defined in code incrementally. It would be nice to have a feature whereby the pipeline could be dynamically understood and executed from a configuration file.

 4. **Logging**: Proper logging would be beneficial for troubleshooting and understanding the pipeline's flow and performance. Currently, there is only minimal print-based logging.
