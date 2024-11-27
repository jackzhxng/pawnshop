from langchain_core.messages.tool import tool_call
from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage, Llama
from typing import List
from prompts import system_prompt, tool_calling_prompt

# From https://github.com/abetlen/llama-cpp-python
llm = Llama(
      model_path="../models/Llama-3.2-3B-Instruct-Q5_K_M.gguf", # https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF
      n_gpu_layers=-1, # Uncomment to use GPU acceleration
      # seed=1337, # Uncomment to set a specific seed
      n_ctx=100000, # Uncomment to increase the context window
      verbose=False,
)

# ====== Chat generation example =======
# out = llm.create_completion(
#   seed=-1,
#   max_tokens=500,
#   prompt=f"{system_prompt} \n\nShopkeeper: Hi, how are you? How can I help you? \n\nErik:",
#   stop="Shopkeeper:"
# )

class LlamaCppAgent:
  # Stores chat history
  messages: List[ChatCompletionRequestMessage] = []

  def __init__(self) -> None:
    self.llm = llm
    self.messages = []

  def generate_chat(self, input_message: str):
    """
    What the user uses - has the agent do everything it needs to do
    (LLM queries, tool calls, etc.) in order to arrive at a suitable
    response to the user.
    """
    print("Calling generate_chat...")
    self.messages.append(ChatCompletionRequestUserMessage(role="user", content=input_message))
    # message_history = '\n\n'.join(self.messages)
    # prompt = f"{system_prompt} \n\n{message_history} \n\nErik:"
    # out = llm.create_completion(
    #   seed=-1,
    #   max_tokens=500,
    #   prompt=prompt,
    #   stop="\n"
    # )

    messages_with_prompt = [ChatCompletionRequestSystemMessage(role="system", content=system_prompt)]
    messages_with_prompt.extend(self.messages)
    out = llm.create_chat_completion(
      seed=-1,
      messages=messages_with_prompt
    )
    # print(f"[DEBUG - prompt]: {prompt}")
    print("======================================")
    print(out)
    agent_message = out["choices"][0]["message"]
    self.messages.append(ChatCompletionRequestAssistantMessage(role="assistant", content=agent_message))
    return self.messages[-1]

  def generate_tool_call(self):
    messages_with_prompt = [ChatCompletionRequestSystemMessage(role="system", content=tool_calling_prompt)]
    messages_with_prompt.extend(self.messages)
    out = llm.create_chat_completion(
      seed=-1,
      max_tokens=500,
      messages=messages_with_prompt,
      tools=[{
          "type": "function",
          "function": {
              "name": "Sell",
              "parameters": {
                  "type": "object",
                  "title": "Sell item",
                  "properties": {
                      "name": {
                          "title": "Name",
                          "type": "string"
                      },
                      "price": {
                          "title": "Price",
                          "type": "integer"
                      }
                  },
                  "required": [ "name", "price" ]
              }
          }
      }]
    )
    print(out)


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

      tool_response = agent.generate_tool_call()
      print(tool_response)

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

