from chat_no_langchain_tool_call import LlamaCppAgent
tool_example= """
TOOL_EAXMPLE = "You will receive a JSON string containing a list of callable tools. Please parse this JSON string and return a JSON object containing the tool name and tool parameters. Here is an example of the tool list:\n\n{"tools": [{"name": "plus_one", "description": "Add one to a number", "parameters": {"type": "object","properties": {"number": {"type": "string","description": "The number that needs to be changed, for example: 1","default": "1",}},"required": ["number"]}},{"name": "minus_one", "description": "Minus one to a number", "parameters": {"type": "object","properties": {"number": {"type": "string","description": "The number that needs to be changed, for example: 1","default": "1",}},"required": ["number"]}}]}\n\nBased on this tool list, generate a JSON object to call a tool. For example, if you need to add one to number 77, return:\n\n{"tool": "plus_one", "parameters": {"number": "77"}}\n\nNote that the above is just an example and does not mean that the plus_one and minus_one tools are currently available."
"""

return_format = """
{"tool": "tool name", "parameters": {"parameter name": "parameter value"}}
"""

available_tools = """
{
  "tools": [
  { 
    "name": "move_forward", 
    "description": "Move forward by 1 position. Moves out of range of Ogre1's attack.",
    "parameters": { 
      "type": "object", 
      "properties": { 
        "character": {
          "type": "string",
          "description": "Which character is performing this action"
        }
      },
    }
  },
  { 
    "name": "move_backward", 
    "description": "Move backward by 1 position. Swaps positions with Erik. Moves out of range of Ogre1's attack, and moves Erik into range of Ogre1's attack.",
    "parameters": { 
      "type": "dict", 
      "required": ["character"]
      "properties": { 
        "character": {
          "type": "string",
          "description": "Which character is performing this action"
        }
      },
    }
  },
  {
    "name": "lunge",
    "description": "Lunges forward, attacking positions 5 and 6. Targets goblin1 and goblin2",
    "parameters": {
      "type": "dict",
      "required": ["character"]
      "properties": {
        "character": {
          "type": "string",
          "description": "Which character is performing this action"
        }
      },
    }
  },
  {
    "name": "dagger_throw",
    "description": "Throws a dagger at position 7, crippling the enemy at that position. Targets ogre1",
    "parameters": {
      "type": "dict",
      "required": ["character"]
      "properties": {
        "character": {
          "type": "string",
          "description": "Which character is performing this action"
        }
      },
    }
  }
  ]
}
"""

# Traditional tools
  # { 
  #   "name": "move_to_position", 
  #   "description": "Move to a position. If there is already a unit there, swap positions with that unit",
  #   "parameters": { 
  #     "type": "object", 
  #     "properties": { 
  #       "position": {
  #         "type": "integer",
  #         "description": "The position number to move to",
  #       },
  #       "thought": {
  #         "type": "string",
  #         "description": "The rationale behind making this decision, expressed in first-person (e.g. I should dispatch this enemy quickly)",
  #       }
  #     },
  #     "required": ["entity_id"]
  #   }
  # },
  # {
  #   "name": "attack_entity_melee",
  #   "description": "Attacks the entity with a melee attack",
  #   "parameters": {
  #       "type": "object",
  #       "properties": {
  #         "entity_id": {
  #           "type": "string",
  #           "description": "The ID of the entity to attack",
  #         },
  #         "thought": {
  #           "type": "string",
  #           "description": "The rationale behind making this decision, expressed in first-person (e.g. I should dispatch this enemy quickly)",
  #         }
  #       },
  #     "required": ["entity_id"]
  #     }
  # },

combat_mechanics = """
Positioning: Combatants occupy specific positions within their party's formation. Position impacts the abilities they can use and their vulnerability to attacks. The player's party has four positions (1–4 from front to back), while the enemy party typically has four mirrored positions.
"""

system_prompt = f"""
You are a game-controller managing the actions of AI characters in a combat scenario. Here is a description of the combat mechanics of the world:
{combat_mechanics}
"""

# TODO: Replace this with Jinja template
def get_thought_prompt(character: str): 
  return """
Based on the combat context, available actions, and character relations, generate the thought process and action for {0} to take using the following format:
Thought: <{0}'s thought>
Action: <{0}'s action, in imperative tense>

Generate a response in imperative tense describing the action that {0} should take, in third person. If the action has storytelling potential, include the line of dialogue that {0} should say. Only perform a single action.

Example:
Thought: {0} would prioritize their ally's safety, given their strong bond. {0} is shielded, so they won't take any damage from an incoming attack.
Action: Move {0} backward to position them to take the force of the incoming attack with dialogue "I'll take this hit, buddy!"
""".format(character) + f"""

Here are your available tools:
{available_tools}
"""

# TODO: Replace this with Jinja template
def get_tool_calling_prompt(character: str):
  return """
Act as the character {0} during a combat encounter. Generate JSON responses to choose the best combat options at the given moment in battle, given the combat context. Generate a JSON response only. Do not generate anything extra.
""".format(character) + f"""
Use the following format:
{return_format}

Here are your available tools:
{available_tools}

Please choose the appropriate tool according to the combat situation.
"""

combat_context = """
Positions:

Ally-side:
1. empty
2. JoeBob
3. Erik
4. empty

Enemy-side:
1. Goblin1
2. Goblin2
3. Ogre1
4. empty

Character Context:
JoeBob:
- Low health

Erik:
- Low health
- Vulnerable to strong attacks

Character Relations:
- Erik views JoeBob as an unreliable ally but respects his resourcefulness in dire situations. He harbors lingering resentment over a past betrayal, yet feels a sense of obligation to protect him, stemming from their shared history as childhood friends.
- JoeBob hates Erik and will find any opportunity to betray him.

Combat context:
- Ogre1 intends to attack position 2 (JoeBob) for high damage
"""

if __name__ == "__main__":
  agent = LlamaCppAgent(system_prompt)
  # response = agent.generate_user_message(combat_context, get_thought_prompt("Erik"))
  # response = agent.generate_chat(get_tool_calling_prompt("Erik"))

  agent.generate_user_message(combat_context, get_thought_prompt("JoeBob"))
  agent.generate_chat(get_tool_calling_prompt("JoeBob"))
