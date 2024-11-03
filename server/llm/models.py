"""
Different models that we have tried out / are using.
"""

import os

from langchain_ollama.chat_models import ChatOllama
from llm.prompts import prompt_template


"""Default"""
def get_default_llm():
    return get_llama_3_2_3b()


"""Cloud"""

def get_open_ai_llm():
    from dotenv import load_dotenv
    from langchain_openai import ChatOpenAI

    load_dotenv()
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    return ChatOpenAI(
        model="gpt-4-turbo",
        api_key=OPENAI_KEY
    )

"""Local"""

def get_llama_3_2_3b():
    # The number of layers to put on the GPU. The rest will be on the CPU.
    # If you don't know how many layers there are, you can use -1 to move
    # all to GPU.
    n_gpu_layers = -1
    n_batch = 512  # Tokens processed in parallel, default val from Llama.cpp docs.
    return ChatOllama(
        model="llama3.2",  # Another option is qwen2.5:1.5b, which has good tool-calling but is bad elsewhere.
        n_batch=n_batch,
        f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls.
        verbose=True,  # Verbose is required to pass to the callback manager.
        n_gpu_layers=n_gpu_layers,
        template=prompt_template
    )

