import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")


@tool
def walk(destination: str):
    """
    Walk to the provided destination. Walking is on average 1 mile per hour.
    """
    print(f"I AM WALKING TO {destination}")
    pass


@tool
def run(destination: str):
    """
    Run to the provided destination. Running is a faster mode of transportation
    than walking.
    """
    print(f"I AM RUNNING TO {destination}")
    pass


@tool
def search_distance(destination: str):
    ""n
    Find out how far from the user the destination is in miles.
    """
    print(f"I AM SEARCHING HOW LONG IT TAKES TO GET TO {destination}")
    return 6


llm = ChatOpenAI(api_key=OPENAI_KEY, model="gpt-4-turbo")

tools = [walk, run, search_distance]
model_with_tools = llm.bind_tools(tools)
query = "I need to get to MPK 17 as fast as possible. Can you help me?"
messages = [HumanMessage(query)]

ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    selected_tool = {
        "walk": walk,
        "run": run,
        "search_distance": search_distance
    }[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

ai_msg = model_with_tools.invoke(messages)
messages.append(ai_msg)
print(messages)
