"""
Main AI agent class.
"""

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic_core._pydantic_core import ValidationError

from llm.prompts import system_prompt, prompt_template
from llm import actions


MAX_RETRIES = 5

class ToolDoesNotExist(Exception):
    pass

class LLMAgent:
    # Stores chat history.
    # TODO: implement memory.
    messages = []

    def __init__(self, llm, tools):
        # The number of layers to put on the GPU. The rest will be on the CPU.
        # If you don't know how many layers there are, you can use -1 to move
        # all to GPU.
        n_gpu_layers = -1
        n_batch = 1024  # Tokens processed in parallel, default val from Llama.cpp docs.
        self.llm = llm
        self.tools = tools
        self.llm = llm.bind_tools(tools)
        self.prompt_template = ChatPromptTemplate([
            ("system", system_prompt),
            MessagesPlaceholder("messages")
        ])

    def generate_chat(self, input_message: str):
        """
        What the user uses - has the agent do everything it needs to do
        (LLM queries, tool calls, etc.) in order to arrive at a suitable
        response to the user.
        """
        print("Calling generate_chat...")
        self.messages.append(HumanMessage(input_message))
        generated_messages = []
        for i in range(MAX_RETRIES):
            try:
                ai_thought_msg = self.generate_chat_response(self.messages)
                print(f"ai_thought_msg: {ai_thought_msg}")
                generated_messages.append(ai_thought_msg)
                if len(ai_thought_msg.tool_calls) > 0:
                    ai_tool_result_msg = self.call_tools(ai_thought_msg)
                    generated_messages.append(ai_tool_result_msg)
                    ai_tool_result_observation_msg = self.generate_chat_response(self.messages + generated_messages) # TODO: to have chained tool calls, this should be recursive.
                    generated_messages.append(ai_tool_result_observation_msg)
            except ToolDoesNotExist as e:
                print(f"{e} - Retrying ({i + 1}/{MAX_RETRIES})")
                continue
            except ValidationError as e:
                print(f"Incorrect function call params were generated: {e}")
                continue
            except Exception as e:
                # If there's other exceptions let's terminate and add handling logic.
                print(f"ALERT: new type of validation error: {type(e)}, please add handling logic.")
                raise(e)

            # Return if everything went smoothly.
            self.messages.extend(generated_messages)
            return self.messages[-1].content

        # Was unable to successfully generate a response after MAX_RETRIES.
        unsuccessful_message = "I don't know what to say to that..."
        self.messages.extend(AIMessage(unsuccessful_message))
        return unsuccessful_message

    def generate_chat_response(self, messages):
        """
        A single query to the LLM.
        """
        print("Calling generate_chat_response...")
        prompt = self.prompt_template.invoke({"messages": messages})
        output = self.llm.invoke(prompt)
        print("Content: ", output.content)
        print("Tool calls: ", output.tool_calls)
        return output

    def call_tools(self, ai_msg):
        """
        Invoke all the tools with the specified arguments
        """
        print("Calling call_tools...")
        for tool_call in ai_msg.tool_calls:
            selected_tool_name = tool_call["name"].lower()
            try:
                tool_function = getattr(actions, selected_tool_name)
                tool_result = tool_function.invoke(tool_call) # TODO: raise error for incorrectly formatted args as well.
                # TODO: just return one for now.
                return tool_result
                self.messages.append(f"Reslt of using tool \"{selected_tool_name}\": {tool_result}") # TODO: There's probably a better way to format this to make it clear that it was the result of a tool.
            except AttributeError:
                raise ToolDoesNotExistException(error_msg)

