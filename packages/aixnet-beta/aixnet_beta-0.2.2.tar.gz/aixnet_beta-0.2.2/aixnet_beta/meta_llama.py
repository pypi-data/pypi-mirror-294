import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

class MetaLlama:
    def __init__(self, azure_inference_endpoint: str, azure_inference_credential: str, protocol: str, max_token: float = 4096):
        self.AZURE_INFERENCE_ENDPOINT = azure_inference_endpoint
        self.AZURE_INFERENCE_CREDENTIAL = azure_inference_credential
        self.protocol = protocol
        self.max_token = max_token
        self.history = [{"role": "user", "content": self.protocol}]
        self.client = ChatCompletionsClient(
            endpoint=self.AZURE_INFERENCE_ENDPOINT,
            credential=AzureKeyCredential(self.AZURE_INFERENCE_CREDENTIAL)
        )

    def list_models(self):
        """Lists the available models for inference."""
        try:
            deployments = self.client.get_model_info()
            for deployment in deployments:
                print("Model name:", deployment.model_name)
                print("Model type:", deployment.model_type)
                print("Model provider name:", deployment.model_provider_name)
        except Exception as e:
            print(f"Error listing models: {e}")

    def add_message(self, role: str, content: str):
        """Adds a message to the history."""
        self.history.append({"role": role, "content": content})

    def invoke_api(self, prompt: str) -> str:
        """
        Invokes the Azure Chat Completions API with the given prompt.

        Args:
            prompt (str): The user prompt to send to the API.

        Returns:
            str: The assistant's response from the API.
        """
        self.add_message("user", prompt)
        try:
            response = self.client.complete(
                messages=self.history,
                max_tokens=self.max_token,
                temperature=0.8,
                top_p=0.1,
                presence_penalty=0
            )
            answer = response.choices[0].message.content
            self.add_message("assistant", answer)
            return answer
        except Exception as e:
            print(f"Error invoking API: {e}")
            return "Sorry, there was an error processing your request."

    def clear_history(self) -> str:
        """Clears the chat history and returns a confirmation message."""
        self.history = [{"role": "user", "content": self.protocol}]
        return "History cleared"

    def get_history(self) -> list:
        """Returns the chat history."""
        return self.history

    def start_chat(self):
        """
        Starts an interactive chat loop with the user.
        Users can type 'EXIT' to end the chat session.
        """
        prompt = ""
        print("🤖 Start chatting with us! Enter 'EXIT' to quit. 🛑")
        while True:
            prompt = input("🧑 Human: ")
            if prompt.upper() == "EXIT":
                break
            response = self.invoke_api(prompt)
            if response:
                print("🤖 Bot:", response)
        print("🙌 Thank you for using the chatbot! Have a great day! 🌟")