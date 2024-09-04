import requests
import json
from typing import Dict, Any


class OpenAIClient:
    """
    A client class for interacting with the OpenAI API and managing a chat session.
    """

    def __init__(self, api_key: str):
        """
        Initializes the OpenAIChatbot with the authorization key.

        Args:
            api_key (str): The authorization API key for OpenAI.
        """
        self.api_url = "https://lwg2c7ib6k.execute-api.us-east-1.amazonaws.com/dev/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"  # The custom AIXNET API Key to be verified by the Lambda function
        }
        self.conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]  # Initialize with a system message

    def invoke_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invokes the OpenAI API with the given payload using a POST request.

        Args:
            payload (Dict[str, Any]): The JSON payload to send with the POST request.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        try:
            # Print the request details for debugging
            # print("Sending request to OpenAI API...")
            # print(f"URL: {self.api_url}")
            # print(f"Headers: {self.headers}")
            # print(f"Payload: {json.dumps(payload, indent=4)}")

            # Send the POST request to the API
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Parse and return the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Print any errors that occur
            print(f"An error occurred: {e}")
            print(f"Response content: {response.content.decode() if response else 'No response'}")
            return {}

    def start_chatting(self):
        """
        Starts a chat session with the user.
        The session continues until the user types 'EXIT'.
        """
        print("🤖 Chatbot is ready! Type 'EXIT' to end the chat.")
        
        while True:
            # Get user input
            user_input = input("👤 Human: ")

            # Exit the loop if the user types 'EXIT'
            if "EXIT" in user_input:
                print("👋 Chatbot session ended. Goodbye!")
                break

            # Append user input to the conversation history
            self.conversation_history.append({"role": "user", "content": user_input})

            # Define the payload for the request using the updated conversation history
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": self.conversation_history,
                "temperature": 0.7
            }

            # Invoke the API and get the response
            response = self.invoke_api(payload)

            # Check if response is valid and print the response from the API
            if response and "choices" in response:
                bot_response = response["choices"][0]["message"]["content"]
                print(f"🤖 Bot: {bot_response}")

                # Append bot response to the conversation history
                self.conversation_history.append({"role": "assistant", "content": bot_response})
            else:
                print("🤖 Bot: Sorry, I didn't understand that. Please try again.")


if __name__ == "__main__":
    # Initialize the OpenAIChatbot with the API key
    api_key = "alex123"  # Replace with your actual API key
    chatbot = OpenAIChatbot(api_key)

    # Start the chat session
    chatbot.start_chatting()
