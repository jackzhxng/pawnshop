from llm.constants import system_prompt, template
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama.chat_models import ChatOllama


@tool
def offer(item: str, price: float):
    """
    Seller offers an item for sale at a given price.
    """
    print(f"OFFERING {item} FOR {price}")
    pass


@tool
def sell(item: str, price: float):
    """
    Seller sells an item at a given price. This can only be done after the
    shopkeeper has accepted an offer
    """
    print(f"SELLING {item} FOR {price}")
    pass


@tool
def rescind_offer(item: str):
    """
    Rescind an offer for an item. This means the seller is no longer willing to
    sell the item.
    """
    print(f"RESCINDING OFFER FOR {item}")
    pass


@tool
def leave_shop():
    """
    Leave the shop. This means the seller is no longer interested in selling
    anything and ends the conversation.
    """
    print("LEAVING SHOP")
    pass


@tool
def state_name(name: str):
    """
    States your name
    """
    print("MY NAME IS", name)
    pass


class LLMAgent:
    # Stores chat history
    messages = []

    def __init__(self):
        # The number of layers to put on the GPU. The rest will be on the CPU.
        # If you don't know how many layers there are, you can use -1 to move
        # all to GPU.
        n_gpu_layers = -1
        # Should be between 1 and n_ctx, consider the amount of RAM of your
        # Apple Silicon Chip.
        n_batch = 1024
        # Make sure the model path is correct for your system!
        llm = ChatOllama(
            model="llama3.2",
            n_batch=n_batch,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            verbose=True,  # Verbose is required to pass to the callback manager
            # n_gpu_layers=n_gpu_layers,
            template=template
        )
        tools = [offer, sell, rescind_offer, leave_shop, state_name]
        self.llm = llm.bind_tools(tools)
        self.prompt_template = ChatPromptTemplate([
            ("system", system_prompt),
            MessagesPlaceholder("msgs")
        ])

    def generate_chat(self, input_message):
        self.messages.append(HumanMessage(input_message))
        ai_msg = self.generate_chat_response()
        if len(ai_msg.tool_calls) > 0:
            self.call_tools(ai_msg)
            ai_msg = self.generate_chat_response()
        return ai_msg.content

    def generate_chat_response(self):
        prompt = self.prompt_template.invoke({"msgs": self.messages})
        ai_msg = self.llm.invoke(prompt)
        self.messages.append(ai_msg)
        return ai_msg

    def call_tools(self, ai_msg):
        for tool_call in ai_msg.tool_calls:
            tools = {
                "offer": offer,
                "sell": sell,
                "rescind_offer": rescind_offer,
                "leave_shop": leave_shop,
                "state_name": state_name
            }
            selected_tool_name = tool_call["name"].lower()
            if selected_tool_name in tools:
                selected_tool = tools[selected_tool_name]
                tool_msg = selected_tool.invoke(tool_call)
                self.messages.append(tool_msg)
            else:
                print("No tool found for ", selected_tool_name)
