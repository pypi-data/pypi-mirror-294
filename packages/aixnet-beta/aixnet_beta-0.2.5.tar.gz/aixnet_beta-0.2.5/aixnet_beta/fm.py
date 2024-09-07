import requests

class AzureFM:
    def __init__(self, model: str, api_key: str, protocol: str):
        self.model = model
        self.api_key = api_key
        self.protocol = protocol
        self.history = [{"role": "system", "content": self.protocol}]
        self.function_key = "vwOe_Up7AAb3L655byywHnTLBZSpfNIo-ohf0p1jTyiwAzFus-C5mA%3D%3D"
        self.url = "https://aixnet1function8.azurewebsites.net/api/http_trigger"

    def list_models(self):
        """
        Prints out the available models.
        """
        models = ['gpt-3.5-turbo', 'meta-llama/Llama-3-8b-chat-hf', 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo']
        print("Available models:", models)

    def add_message(self, role: str, content: str):
        """
        Appends a message to the history.
        """
        self.history.append({"role": role, "content": content})

    def invoke_api(self, prompt: str) -> str:
        """
        Makes an API call to the Azure Function with the given prompt.
        Uses try-except to handle potential errors.
        """
        self.add_message("user", prompt)

        payload = {
            "model": self.model,
            "api_key": self.api_key,
            "messages": self.history
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(f"{self.url}?code={self.function_key}", json=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Try to parse the response as JSON
                try:
                    response_data = response.json()
                    bot_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    self.add_message("assistant", bot_response)
                    return bot_response
                except ValueError:
                    # If JSON parsing fails, assume the response is plain text
                    bot_response = response.text
                    self.add_message("assistant", bot_response)
                    return bot_response
            else:
                # If the status code is not 200, return the status and response text
                return f"Error: Received status code {response.status_code}\nResponse text: {response.text}"
        except Exception as e:
            # Catch any other errors
            return f"An error occurred: {str(e)}"

    def clear_history(self) -> str:
        """
        Resets the conversation history to the initial state.
        """
        self.history = [{"role": "system", "content": self.protocol}]
        return "History cleared."

    def get_history(self) -> list:
        """
        Returns the conversation history.
        """
        return self.history

    def start_chat(self):
        """
        Starts an interactive chat loop with the user.
        Users can type 'EXIT' to end the chat session.
        """
        print("🤖 Start chatting with us! Enter 'EXIT' to quit. 🛑")
        while True:
            prompt = input("🧑 Human: ")
            if prompt.upper() == "EXIT":
                break
            response = self.invoke_api(prompt)
            if response:
                print("🤖 Bot:", response)
        print("🙌 Thank you for using the chatbot! Have a great day! 🌟")
