from llm.constants import system_prompt, template
from typing import Literal
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama.chat_models import ChatOllama


@tool
def make_offer(
    price: float,
    item: str,
    offer_type: Literal["buy", "sell"],
    context: str = None
) -> dict:
    """
    Make or counter an offer for an item. This starts a negotiation interaction
    with the shopkeeper.
    Context allows adding reasoning/justification for the price.
    Returns {"accepted": bool, "counter_price": float | None, "message": str}
    """
    print("[TOOL CALL]")
    print(f"Making {offer_type} offer: {item} for {price} ({context})")


@tool
def inspect_item(
    item: str,
    aspect: Literal["quality", "history",
                    "authenticity", "market_value"]
) -> dict:
    """
    Examine an item and get information about it.
    Returns {"info": str, "estimated_value": float, "condition": str}
    """
    print("[TOOL CALL]")
    print(f"Inspecting {item} for {aspect}")


@tool
def negotiate_terms(
    action: Literal[
        "request_discount",
        "bundle_items",
        "highlight_value",
        "point_out_flaws"
    ],
    item: str,
    justification: str
) -> dict:
    """
    Perform a negotiation action with justification.
    Actions can be one of the following: request_discount, bundle_items, highlight_value, point_out_flaws
    Returns {"success": bool, "response": str, "modified_price": float | None}
    """
    print("[TOOL CALL]")
    print(f"{action}: {item} - Justification: {justification}")


# @tool
# def express_intent(
#     emotion: Literal[
#         "interest",
#         "disinterest",
#         "enthusiasm",
#         "frustration",
#         "urgency"
#     ],
#     intensity: int,
#     reason: str
# ) -> dict:
#     """
#     Express an emotion or intent during negotiation.
#     Emotions can be one of the following: interest, disinterest, enthusiasm, frustration, urgency
#     Intensity should be 1-5.
#     Returns {"shopkeeper_response": str, "impact": float}
#     """
#     print("[TOOL CALL]")
#     print(f"Expressing {emotion} ({intensity}): {reason}")


@tool
def social_action(
    action: Literal[
        "build_rapport",
        "share_story",
        "mention_competitor",
        "promise_future_business",
        "appeal_to_fairness"
    ],
    details: str
) -> dict:
    """
    Perform a social action to influence negotiation.
    Actions can be one of the following: build_rapport, share_story, mention_competitor, promise_future_business, appeal_to_fairness

    Returns {"relationship_change": float, "response": str}
    """
    print("[TOOL CALL]")
    print(f"Performing {action}: {details}")


@tool
def conclude_interaction(
    action: Literal["accept", "reject", "walk_away"],
    final_message: str
) -> dict:
    """
    End the current negotiation sequence.
    Actions can be one of the following: accept, reject, walk_away
    Returns {"final_status": str, "deal_made": bool, "final_price": float | None}
    """
    print("[TOOL CALL]")
    print(f"{action}: {final_message}")


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
            # model="qwen2.5:1.5b",
            model="llama3.2",
            n_batch=n_batch,
            f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
            verbose=True,  # Verbose is required to pass to the callback manager
            n_gpu_layers=n_gpu_layers,
            template=template
        )
        tools = [
            make_offer,
            inspect_item,
            negotiate_terms,
            # express_intent,
            social_action,
            conclude_interaction]
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
        print("content: ", ai_msg.content)
        print("tool calls: ", ai_msg.tool_calls)
        return ai_msg

    def call_tools(self, ai_msg):
        for tool_call in ai_msg.tool_calls:
            tools = {
                "make_offer": make_offer,
                "inspect_item": inspect_item,
                "negotiate_terms": negotiate_terms,
                # "express_intent": express_intent,
                "social_action": social_action,
                "conclude_interaction": conclude_interaction
            }
            selected_tool_name = tool_call["name"].lower()
            if selected_tool_name in tools:
                selected_tool = tools[selected_tool_name]
                tool_msg = selected_tool.invoke(tool_call)
                self.messages.append(tool_msg)
            else:
                self.messages.remove(ai_msg)
                print("No tool found for ", selected_tool_name)
