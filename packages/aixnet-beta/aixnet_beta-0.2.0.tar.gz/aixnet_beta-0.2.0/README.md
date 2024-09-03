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

### Example

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

### License

This project is licensed under the MIT License.