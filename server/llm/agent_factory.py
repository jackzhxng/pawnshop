from llm import actions
from llm.models import get_default_llm
from llm.agent import LLMAgent


ERIK_STONEHENGE_CONFIG = """
name: Eric Stonehenge
"""

CUSTOMER_AGENT_BASE_TOOLS = [
    actions.make_offer,
    # actions.inspect_item,
    actions.negotiate_terms,
    # actions.social_action,
    actions.conclude_interaction
]

def create_agent_from_yaml(yaml_str: str) -> LLMAgent:
    yaml = yaml.load(yaml_str)
    return LLMAgent(get_default_llm(), CUSTOMER_AGENT_BASE_TOOLS)
    

def create_test_agent() -> LLMAgent:
    return LLMAgent(get_default_llm(), CUSTOMER_AGENT_BASE_TOOLS)

