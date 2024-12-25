from llm import actions
from llm.models import get_default_llm
from llm.agent import LLMAgent

CUSTOMER_AGENT_BASE_TOOLS = [
    actions.sell,
    actions.leave_shop,
    actions.get_inventory,
]

# If a `buy` tool is defined in actions, include it as well so test agents
# can invoke client-side buys.
if hasattr(actions, "buy"):
    CUSTOMER_AGENT_BASE_TOOLS.append(actions.buy)

def create_agent_from_yaml(yaml_str: str) -> LLMAgent:
    yaml = yaml.load(yaml_str)
    return LLMAgent(get_default_llm(), CUSTOMER_AGENT_BASE_TOOLS)    

def create_test_agent() -> LLMAgent:
    return LLMAgent(get_default_llm(), CUSTOMER_AGENT_BASE_TOOLS)

