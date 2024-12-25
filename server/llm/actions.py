"""
All the tools that the agent can call which form its action space.
"""


from langchain.tools import tool
from typing import Dict, Literal

from pydantic import BaseModel, Field


@tool
def buy(
    item: str,
    price: int,
    quantity: int,
) -> bool:
    """
    Buys a specified number of the specified item at the specified price.
    """
    # Some database call here.
    return True

class SellInput(BaseModel):
    item: str = Field(description="The name of the item being sold (e.g., 'Iron Sword')")
    price: int = Field(description="The price per unit in gold coins. Must be a positive integer.")
    quantity: int = Field(description="How many units to sell.")

@tool(args_schema=SellInput)
def sell(item: str, price: int, quantity: int) -> str:
    """
    Executes a sale. Use this ONLY after the player has explicitly accepted the offer.
    """
    # Logic here
    return f"Successfully sold {quantity} {item}(s) for {price} gold each."

@tool
def leave_shop() -> bool:
    """
    Leaves the shop and concludes interactions with the shopkeeper.
    """
    return True


# Tools that must be executed by the client (Godot) instead of locally on the server.
# These names should be lowercased and match tool_call["name"].
# Mark shop-interaction tools remote so the Godot client executes them and
# returns structured results back to the server.
REMOTE_TOOLS = {"get_inventory", "sell", "buy", "leave_shop"}

@tool
def get_inventory(npc_id: str) -> str:
    """
    (Client-side) Returns the inventory for the given NPC. This tool is intended
    to be executed by the Godot client and sent back to the server. On the
    server side this is a placeholder and should not be invoked locally.
    """
    # Placeholder; when marked remote, the LLMAgent will not call this locally.
    return ""

