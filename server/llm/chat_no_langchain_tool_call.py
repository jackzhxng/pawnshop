from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage, Llama
from typing import List
from prompts import system_prompt 

import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# From https://github.com/abetlen/llama-cpp-python
llm = Llama(
      model_path="../models/Llama-3.2-3B-Instruct-Q5_K_M.gguf", 
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
      n_ctx=100000, # Uncomment to increase the context window
      verbose=False,
)


class LlamaCppAgent:
  # Stores chat history
  messages: List[ChatCompletionRequestMessage] = []

  def __init__(self) -> None:
    self.llm = llm
    self.messages = []

  def get_messages_with_system_prompts(self, system_prompts: List[str]):  
    """
    Returns the message history with the specified system prompt prepended to it.
    Allows us to dynamically switch out system prompts
    """
    messages_with_prompt: List[ChatCompletionRequestMessage] = [
      ChatCompletionRequestSystemMessage(role="system", content=system_prompt) 
      for system_prompt in system_prompts
    ]
    messages_with_prompt.extend(self.messages)
    return messages_with_prompt


  def generate_chat(self, input_message: str):
    """
    What the user uses - has the agent do everything it needs to do
    (LLM queries, tool calls, etc.) in order to arrive at a suitable
    response to the user.
    """
    logger.debug(f"Generating responses with messages: {self.messages}")
    self.messages.append(ChatCompletionRequestUserMessage(role="user", content=input_message))
    messages_with_prompt = self.get_messages_with_system_prompts([system_prompt])
    out = llm.create_chat_completion( seed=-1, # Sets random seed every time, so makes completion non-deterministic
      messages=messages_with_prompt
    )
    logger.debug(out)

    agent_message = out["choices"][0]["message"]
    self.messages.append(ChatCompletionRequestAssistantMessage(role="assistant", content=agent_message))
    return self.messages[-1]


if __name__ == "__main__":
  agent = LlamaCppAgent()

  try:
    while True:
      user_input = input("Enter your message (or 'quit' to exit): ")

      if user_input.lower() == 'quit':
        print("Exiting the chat session.")
        break

      try:
        response = agent.generate_chat(user_input)
        print(f"{response}")
      except Exception as e:
          print(f"An error occurred: {str(e)}")

  except KeyboardInterrupt:
    print("\nChat session interrupted by user.")
  except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")

 

#  ============ Function calling example ============
# out = llm.create_chat_completion(
#   seed=-1,
#   messages = [
#       {
#         "role": "system",
#         "content": system_prompt
#       },
#       {
#         "role": "user",
#       "content": "Shopkeeper: Hi, how are you? Erik:"
#       }
#   ],
  # tools=[{
  #     "type": "function",
  #     "function": {
  #         "name": "Sell",
  #         "parameters": {
  #             "type": "object",
  #             "title": "Sell",
  #             "properties": {
  #                 "name": {
  #                     "title": "Name",
  #                     "type": "string"
  #                 },
  #                 "age": {
  #                     "title": "Age",
  #                     "type": "integer"
  #                 }
  #             },
  #             "required": [ "name", "age" ]
  #         }
  #     }
  # }]
    # tool_choice={
    #   "type": "function",
    #   "function": {
    #     "name": "UserDetail"
    #   }
    # }
# )

# print(out)
# print(out["choices"][0]["message"])

# ====== Chat generation example =======
# out = llm.create_completion(
#   seed=-1,
#   max_tokens=500,
#   prompt=f"{system_prompt} \n\nShopkeeper: Hi, how are you? How can I help you? \n\nErik:",
#   stop="Shopkeeper:"
# )
