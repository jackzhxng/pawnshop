"""
All the tools that the agent can call which form its action space.
"""

from langchain.tools import tool
from typing import Dict, Literal


# @tool
# def buy(
#     item: str,
#     price: int,
#     quantity: int,
# ) -> bool:
#     """
#     Buys a specified number of the specified item at the specified price.
#     """
#     # Some database call here.
#     return True

@tool
def sell(
    item: str,
    price: int,
    quantity: int,
) -> bool:
    """
    Sells a specified number of the specified item at the specified price.
    """
    # Some database call here.
    return True

@tool
def leave_shop() -> bool:
    """
    Leaves the shop and concludes interactions with the shopkeeper.
    """
    return True

