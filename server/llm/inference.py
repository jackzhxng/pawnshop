import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

print(f"OPENAI_KEY: {OPENAI_KEY}")

class LLM:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            api_key=OPENAI_KEY
        )

    def infer(self, prompt: str):
        return self.llm.invoke(prompt).content

