from openai import OpenAI  # Ensure correct OpenAI library is imported

class NvidiaClient:
    def __init__(
        self,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        model_name: str = "nv-mistralai/mistral-nemo-12b-instruct",
        protocol: str = "You are a helpful assistant.",
        api_key: str = ""
    ):
        if not api_key:
            raise ValueError("API key must be provided.")
        
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(
            base_url=base_url,
            api_key=self.api_key
        )
        self.history = [{"role": "system", "content": protocol}]

    def list_models(self):
        # This method prints a static list of models for demonstration purposes.
        content = f"""
        List of models:
        - mistralai/mistral-large-2-instruct
        - nv-mistralai/mistral-nemo-12b-instruct
        - meta/llama-3.1-8b-instruct
        
        Current model:
        {self.model_name}
        """
        print(content)

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def invoke_api(self, prompt: str):
        self.add_message("user", prompt)
        try:
            # Assuming correct method usage for chat completion
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.history,
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )
            
            answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    answer += chunk.choices[0].delta.content
            
            self.add_message("assistant", answer)
            return answer
        
        except Exception as e:
            print(f"An error occurred while invoking the API: {e}")
            return None

    def clear_history(self):
        self.history = [{"role": "system", "content": self.protocol}]

    def get_history(self):
        return self.history

    def start_chat(self):
        """
        Start an interactive chat loop with the user.
        Users can type 'EXIT' to end the chat session.
        """
        prompt = ""
        print("🤖 Start chatting with us! Enter 'EXIT' to quit. 🛑")
        while "EXIT" not in prompt:
            prompt = input("🧑 Human: ")
            if "EXIT" in prompt:
                break
            response = self.invoke_api(prompt)
            if response is not None:
                print("🤖 Bot: " + response)
        print("🙌 Thank you for using the chatbot! Have a great day! 🌟")
