from llm import actions
from llm.models import get_default_llm
from llm.agent import LLMAgent


ERIK_STONEHENGE_CONFIG = """
name: Eric Stonehenge
"""

CUSTOMER_AGENT_BASE_TOOLS = [
    # actions.buy,
    actions.sell,
    actions.leave_shop,
]

def create_agent_from_yaml(yaml_str: str) -> LLMAgent:
    yaml = yaml.load(yaml_str)
    return LLMAgent(get_default_llm(), CUSTOMER_AGENT_BASE_TOOLS)    

def create_test_agent() -> LLMAgent:
    return LLMAgent(get_default_llm(), CUSTOMER_AGENT_BASE_TOOLS)

