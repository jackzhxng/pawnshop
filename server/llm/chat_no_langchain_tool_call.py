from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage, Llama
from typing import List
import re


# From https://github.com/abetlen/llama-cpp-python
llm = Llama(
      model_path="../models/Llama-3.2-3B-Instruct-Q5_K_M.gguf", 
      # model_path="../models/OrcaAgent-llama3.2-8b.Q5_K_M.gguf", 
      # model_path="../models/Mistral-Small-Instruct-2409-IQ4_XS.gguf", 
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
      n_ctx=8000, # Uncomment to increase the context window
      verbose=False,
)

class LlamaCppAgent:
  # Stores chat history
  messages: List[ChatCompletionRequestMessage] = []

  def __init__(self, system_prompt: str) -> None:
    self.llm = llm
    self.messages = []
    self.system_prompt = system_prompt

  def generate_chat(self, prompt: str) -> ChatCompletionRequestMessage:
    """
    What the user uses - has the agent do everything it needs to do
    (LLM queries, tool calls, etc.) in order to arrive at a suitable
    response to the user.
    """
    messages_with_prompt = [{"role":"system", "content":self.system_prompt + prompt}]
    messages_with_prompt.extend(self.messages)
    # self.debug_print_message_history()
    out = llm.create_chat_completion(
      seed=-1,
      messages=messages_with_prompt
    )
    agent_message = out["choices"][0]["message"]["content"]
    self.messages.append({"role":"assistant", "content":agent_message})
    print(self.messages[-1])
    print("======================================")
    return self.messages[-1]

  def generate_user_message(self, input_message: str, prompt: str):
    self.messages.append(ChatCompletionRequestUserMessage(role="user", content=input_message))

    messages_with_prompt = [ChatCompletionRequestSystemMessage(role="system", content=self.system_prompt + prompt)]
    messages_with_prompt.extend(self.messages)
    # self.debug_print_message_history()
    out = llm.create_chat_completion(
      seed=-1,
      messages=messages_with_prompt
    )
    # print(f"[DEBUG - prompt]: {prompt}")
    agent_message = clean_text(out["choices"][0]["message"]["content"])
    self.messages.append({"role":"assistant", "content":agent_message})
    print(self.messages[-1])
    print("======================================")
    return self.messages[-1]

  def debug_print_message_history(self):
    print("--- PREVIOUS MESSAGES ---")
    for msg in self.messages:
      print("[[" + msg['role'] + "]]" + ": " + msg['content'])
      print("---")

def clean_text(text: str)-> str:
    cleaned_text = re.sub(r'\*.*?\*(?!\.\S)', '', text)
    cleaned_text = re.sub(r'\([^\)]*\)', '', cleaned_text)
    return cleaned_text
