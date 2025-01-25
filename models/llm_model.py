from groq import Groq

class LLMModel:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)

    def generate(self, name, llm, work, role, context=""):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "assistant",
                    "content": f"You are {name}, a {role}. Your task is to {work}.\nContext: {context}"
                }
            ],
            model=llm,
        )
        return chat_completion.choices[0].message.content