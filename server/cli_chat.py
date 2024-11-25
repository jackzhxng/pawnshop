#!/usr/bin/env python3

from llm import agent_factory

def chat():
    example_agent = agent_factory.create_test_agent()
    while True:
        # Get user's choice
        user_input = input(">>> ")

        # Check if user wants to exit
        if user_input.lower() == "\q":
            print("Exiting the program.")
            break

        # Process user's input
        print(example_agent.generate_chat(user_input))

if __name__ == "__main__":
    chat()
