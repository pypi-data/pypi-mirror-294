# AIXNet Beta

## Overview

AIXNet Beta is a Python package that provides an interface to interact with the OpenAI API. It simplifies the process by requiring only the API key and the payload to get started.

## Installation

To install the package, use:

```bash
pip install aixnet-beta
```

## Usage

### Step 1: Import the `OpenAIClient` class

```python
from aixnet_beta.fm import OpenAIClient
```

### Step 2: Initialize the client

Initialize the client with your OpenAI API key.

```python
# Replace 'YOUR_API_KEY' with your actual API key
api_key = "YOUR_API_KEY"

# Initialize the OpenAI client
client = OpenAIClient(api_key)
```

### Step 3: Define the payload

Define the payload for your API request. The payload must be a dictionary that represents the request you want to send to the OpenAI API.

```python
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "user", "content": "What is 1+1?"}
    ],
    "temperature": 0.7
}
```

### Step 4: Invoke the API and get the response

Use the `invoke_api` method of the `OpenAIClient` class to send the request and receive a response.

```python
# Invoke the API and get the response
response = client.invoke_api(payload)

# Print the response from the API
print(json.dumps(response, indent=4))
```

### Example: GPT

Here is a complete example of using the `OpenAIClient`:

```python
from aixnet_beta.fm import OpenAIClient
import json

# Initialize the OpenAI client with the API key
api_key = "alex123"  # Replace with your actual API key
client = OpenAIClient(api_key)

# Define the payload for the request
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Say this is a test!"}
    ],
    "temperature": 0.7
}

# Invoke the API and get the response
response = client.invoke_api(payload)

# Print the response from the API
print(json.dumps(response, indent=4))
```

Alternatively, you can run the code and chat with the foundation model in terminal.

```python
# Initialize the OpenAIClient with the API key
api_key = "alex123"  # Replace with your actual API key
chatbot = OpenAIClient(api_key)

# Start the chat session
chatbot.start_chatting()
```

### Example: Meta LLama

We have implemented the most latest foundation model from Meta. For example, Meta's *Meta-Llama-3-405B-Instruct* is included in this package. You can chat to it directly using the *.start_chat()* method.

```python
AZURE_INFERENCE_ENDPOINT = "ENDPOINT_URL_HERE"
AZURE_INFERENCE_CREDENTIAL = "API_KEY

from aixnet_beta.meta_llama import MetaLlama

bot = MetaLlama(
    AZURE_INFERENCE_ENDPOINT,
    AZURE_INFERENCE_CREDENTIAL,
    "You are a coding assistant. You always use type hints, docstring, and comments in py code.")
bot.start_chat()
```

Here's an expected output:

```
🤖 Start chatting with us! Enter 'EXIT' to quit. 🛑
🧑 Human: write a hello world py func
🤖 Bot: Here is a "Hello World" Python function with type hints, docstring, and comments:
    ```python
    def hello_world(name: str) -> None:
        """
        Prints a personalized "Hello World" message.

        Args:
            name (str): The name to include in the greeting.

        Returns:
            None
        """
        # Print the greeting message
        print(f"Hello, {name}!")

    # Example usage:
    hello_world("Alice")  # Output: Hello, Alice!
    ```
Let me know if you'd like me to explain any part of this code!
🧑 Human: EXIT
🙌 Thank you for using the chatbot! Have a great day! 🌟
```

### License

This project is licensed under the MIT License.