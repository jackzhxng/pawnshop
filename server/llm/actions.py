"""
All the tools that the agent can call which form its action space.
"""

from langchain.tools import tool
from typing import Dict, Literal


@tool
def make_offer(
    price: float,
    item: str,
    offer_type: Literal["buy", "sell"],
    context: str = None
) -> str:
    """
    Make or counter an offer for an item. This starts a negotiation interaction
    with the shopkeeper.
    Context allows adding reasoning/justification for the price.
    Returns {"accepted": bool, "counter_price": float | None, "message": str}
    """
    print("[TOOL CALL]")
    return f"Making {offer_type} offer: {item} for {price} because {context}"


# @tool
# def inspect_item(
#     item: str,
#     aspect: Literal["quality", "history",
#                     "authenticity", "market_value"]
# ) -> dict:
#     """
#     Examine an item and get information about it.
#     Returns {"info": str, "estimated_value": float, "condition": str}
#     """
#     print("[TOOL CALL]")
#     return (f"Inspecting {item} for {aspect}")


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
) -> str:
    """
    Perform a negotiation action with justification.
    Actions can be one of the following: request_discount, bundle_items, highlight_value, point_out_flaws
    """
    print("[TOOL CALL]")
    return f"I will {action.replace('_', ' ')} for {item} because {justification}"


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


# @tool
# def social_action(
#     action: Literal[
#         "build_rapport",
#         "share_story",
#         "mention_competitor",
#         "promise_future_business",
#         "appeal_to_fairness"
#     ],
# ) -> str:
#     """
#     Employ a negotiation strategy.
#     """
#     print("[TOOL CALL]")
#     # e.g. rapport += 1
#     return f"I need to {action.replace('_', ' ')}"


@tool
def conclude_interaction(
    action: Literal["accept", "reject", "walk_away"],
    final_message: str
) -> str:
    """
    End the current negotiation sequence.
    Actions can be one of the following: accept, reject, walk_away
    Returns {"final_status": str, "deal_made": bool, "final_price": float | None}
    """
    print("[TOOL CALL]")
    return f"The negotiation has ended with the following result: {action}: {final_message}"
