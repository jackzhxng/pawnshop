from chat_no_langchain_tool_call import LlamaCppAgent

system_prompt = """You are a dungeon master for a Dungeons and Dragons campaign. Generate a character for the following world: 

The world of Elandria is a land where magic and nature reign supreme. Enchanted forests stretch across vast continents, ancient ruins dot the landscape, and powerful sorcerers harness the elements. Mystical creatures roam the wilderness, while cities built of stone and wood thrive under the protection of guardian spirits. Old gods slumber beneath the earth, their power still felt through forgotten relics. Kingdoms vie for dominance, while ancient prophecies hint at a coming calamity that may unravel the very fabric of magic itself.

Here is an example output:

Grixel "Shatterquill" Blinksnout

Backstory: Escaped a cruel alchemist guild after animating their ledger; now a fugitive selling chaotic inventions.
Ambitions: Build the "Ultimate Contraption" to prove goblin genius and reclaim his stolen invention.
Personality: Hyperactive, inventive, and reckless, viewing failure as a stepping stone to success.
Speaking Style: Extremely rapid, technical, and slangy. For example:
*"Alright, no sweat! Twist the fluxcap, slam the pressure rod, zap the sparkcoil with a teaspoon of dragonfire—BOOM, we’re running like a greased weasel on a hotplate! One flick and we’ll be flying or exploding! Either way, it'll be epic! Just don’t step on the glowing button, okay?"

"Okay! Easy! Jerk the sparkrod, shove the piston into the engine’s belly, and—whoosh—pop the turbo-tubes! Half a second from glory or disaster, but trust me, it’s all the same when you’re GOING! Hold on tight, we’re gonna rip through the sky like a sizzling comet on a caffeine binge!"

Reason for Joining: Sees the mercenary crew as a chance to test inventions in real-world chaos while avoiding guild bounty hunters.

Here is another example:

Lady Persephone Thornbrook ("The Widow of Starlight")

Backstory: Faked her death to escape elven noble politics; roams the world seeking her reincarnated lost love.
Ambitions: Reunite with her lover’s soul and regain her influence through subtle power plays.
Personality: Elegant, melancholic, and manipulative, with a flair for the dramatic.
Speaking Style: Extremely poetic, archaic, and wistful. For example:
"Ah, how the stars weep for what was lost, their silver tears tracing forgotten paths. We are but shadows, fleeting as the breath of the moon herself."

"Can you hear it? The stars call, their voices soft as the night’s embrace. Destiny waits, tangled in the threads of time… and I, I shall be the one to unravel it."

"The ruins whisper, his name lost among the stones. I will find him—I must—for the night shall not pass without him in my arms once more."

Reason for Joining: Uses the mercenary crew to explore distant lands discreetly and expand her influence while searching for her lost love.

Generate another character with the same format. Do not include any extra information.
"""

if __name__ == "__main__":
    agent = LlamaCppAgent(system_prompt)
    agent.generate_user_message("","")
