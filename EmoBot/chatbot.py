# This is a simple chatbot using OpenAI's gpt-4 model.
import openai

class ChatBot:
    def __init__(self, api_key: str, instructions: str, model="gpt-4"):
        self.api_key = api_key
        self.model = "gpt-4"  # Default model
        self.history = [{"role": "system", "content": instructions}]
        openai.api_key = api_key
        self.instructions = instructions

        # Create openAI client
        self.client = openai.OpenAI(api_key=openai.api_key)


    def get_response(self, user_input): 
        self.history.append({"role": "user", "content": user_input})
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history
            )
            reply = response.choices[0].message.content.strip()
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Error: {e}"

