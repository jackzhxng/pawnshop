from langchain_core.messages.tool import tool_call
from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage, Llama
from typing import List
# from prompts import system_prompt, tool_calling_prompt

tool_example= """
TOOL_EAXMPLE = "You will receive a JSON string containing a list of callable tools. Please parse this JSON string and return a JSON object containing the tool name and tool parameters. Here is an example of the tool list:\n\n{\"tools\": [{\"name\": \"plus_one\", \"description\": \"Add one to a number\", \"parameters\": {\"type\": \"object\",\"properties\": {\"number\": {\"type\": \"string\",\"description\": \"The number that needs to be changed, for example: 1\",\"default\": \"1\",}},\"required\": [\"number\"]}},{\"name\": \"minus_one\", \"description\": \"Minus one to a number\", \"parameters\": {\"type\": \"object\",\"properties\": {\"number\": {\"type\": \"string\",\"description\": \"The number that needs to be changed, for example: 1\",\"default\": \"1\",}},\"required\": [\"number\"]}}]}\n\nBased on this tool list, generate a JSON object to call a tool. For example, if you need to add one to number 77, return:\n\n{\"tool\": \"plus_one\", \"parameters\": {\"number\": \"77\"}}\n\nPlease note that the above is just an example and does not mean that the plus_one and minus_one tools are currently available."
"""

return_format = """
{\"tool\": \"tool name\", \"parameters\": {\"parameter name\": \"parameter value\"}}
"""

available_tools = """
{
	"tools": [
		{
			"name": "move_to_entity",
			"description": "Move to be within melee range of an entity",
			"parameters": {
				"type": "object",
				"properties": {
					"entity_id": {
						"type": "string",
						"description": "The ID of the entity to move to",
					},
                    "thought": {
						"type": "string",
						"description": "The rationale behind making this decision, expressed in first-person (e.g. I should dispatch this enemy quickly)",
                    }
				},
				"required": ["entity_id"]
			}
		},
		{
			"name": "attack_entity_melee",
			"description": "Attacks the entity with a melee attack",
			"parameters": {
				"type": "object",
				"properties": {
					"entity_id": {
						"type": "string",
						"description": "The ID of the entity to attack",
					},
                    "thought": {
						"type": "string",
						"description": "The rationale behind making this decision, expressed in first-person (e.g. I should dispatch this enemy quickly)",
                    }
				},
				"required": ["entity_id"]
			}
		},
	]
}
"""


system_prompt = f"""
{tool_example}

Act as the character Erik Stoneforge during a combat encounter. Generate JSON responses to choose the best combat options at the given moment in battle, given the combat context. Generate a JSON response only. Do not generate anything extra.

Use the following format:
{return_format}

Here are your available tools:
{available_tools}

Please choose the appropriate tool according to the combat situation.
"""

thought_system_prompt = f"""
Act as the character Erik Stoneforge during a combat encounter. Generate JSON responses to choose the best combat options at the given moment in battle, given the combat context. Generate a JSON response only. Do not generate anything extra.

Question: What is the elevation range for the area that the eastern sector of the
Colorado orogeny extends into?
Thought: Let’s think step by step. The eastern sector of Colorado orogeny extends
into the High Plains. High Plains rise in elevation from around 1,800 to
7,000 ft, so the answer is 1,800 to 7,000 ft.

Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons"
character Milhouse, who Matt Groening named after who?
Thought: Let’s think step by step. Milhouse was named after U.S. president Richard
Nixon, so the answer is Richard Nixon.
"""

combat_context = """
- Erik Stoneforge (ID: erik) is currently fighting with a goblin (ID: goblin_1)
- There is another goblin (ID: goblin_2) who is further away
"""

# From https://github.com/abetlen/llama-cpp-python
llm = Llama(
      model_path="../models/Llama-3.2-3B-Instruct-Q5_K_M.gguf", 
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

