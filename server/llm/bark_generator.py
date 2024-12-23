from chat_no_langchain_tool_call import LlamaCppAgent

character_4 = """
Nyx Evernight
Backstory: A shadowy rogue from a forgotten guild, Nyx was cast out after she broke their code to save a child. Now, she’s on the run, taking odd jobs to survive, but the mark on her soul remains: the child she saved has disappeared, and Nyx believes the guild is still hunting them both.
Ambitions: To find the child and bring them to safety, and to destroy the guild that betrayed her.
Personality: Mysterious, calculating, and driven by a personal code of justice, albeit one she often keeps hidden. She’s quiet, but when she speaks, it’s sharp and purposeful.
Speaking Style: Soft, clipped, and cryptic, with an air of cold detachment. For example:
"The shadows speak in whispers, but I listen closely. They’re telling me things... things I need to hear. This quest? It’s not about the gold. It’s about finding her—and making sure she never feels the cold hands of that guild again."

Reason for Joining: Seeks the crew’s help to gather information, find the child, and take revenge on the guild without drawing attention to herself.
"""

character_2 = """
Lady Persephone Thornbrook ("The Widow of Starlight")
Backstory: Faked her death to escape elven noble politics; roams the world seeking her reincarnated lost love.
Ambitions: Reunite with her lover’s soul and regain her influence through subtle power plays.
Personality: Elegant, melancholic, and manipulative, with a flair for the dramatic.
Speaking Style: Extremely poetic, archaic, and wistful. For example:
"Ah, how the stars weep for what was lost, their silver tears tracing forgotten paths. We are but shadows, fleeting as the breath of the moon herself."

"Can you hear it? The stars call, their voices soft as the night’s embrace. Destiny waits, tangled in the threads of time… and I, I shall be the one to unravel it."

"The ruins whisper, his name lost among the stones. I will find him—I must—for the night shall not pass without him in my arms once more."

Reason for Joining: Uses the mercenary crew to explore distant lands discreetly and expand her influence while searching for her lost love.
"""

system_prompt = """You are a dungeon master for a Dungeons and Dragons campaign. Generate a set of short barks, following this character's personality and speaking style:
{0}

The barks should be for the following actions. Generate at least 2 for each:
Your turn
Attacking
Taking Damage
Missing an Attack
Defeating an Enemy

Example:
Your turn
"Let’s make this clean. No wasted strikes."
"I’ve fought worse in darker days."
"Time to show them what forged steel can do."

Attacking
"Feel the weight of my hammer!"
"One strike is all I need."

Taking Damage
"Hnh. That all you’ve got?"
"It’ll take more than that to fell me."

Missing an Attack
"You live a moment longer... just a moment."

Defeating an Enemy:
"Fall, as all tyrants do."
"Another wrong righted."
"Your evil ends here."

Keep the barks short and concise. Don't generate anything extra.

""".format(character_2)


if __name__ == "__main__":
    agent = LlamaCppAgent(system_prompt)
    agent.generate_user_message("","")
