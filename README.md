# Pawnshop - Haggle with an LLM-powered NPC!
Inspired by projects like https://arxiv.org/pdf/2304.03442, https://github.com/altera-al/project-sid, and looking to play with AI agents

## Overview
**LLM Integration**: 
- LLM: The system can use OpenAI API (external) or Ollama-hosted models (local) interchangeably.
- Agent Orchestration: The backend uses LangChain to implement custom chains for managing multi-step interactions (chaining reasoning, tools, memory retrieval)
- Vector Store experiments: Experiments with a vector-store memory using FAISS for knowledge retrieval. Includes prototypes for storing conversation context or facts in a FAISS index to prepare for future memory-based recall

**Backend:**
- Uses [Flask](https://flask.palletsprojects.com/en/stable/) as a light HTTP API to expose endpoints

**Frontend**
- Game client is built with the [Godot Engine](https://godotengine.org/) which provides the UI, character portraits, and input / output for dialogue.
- Uses Godot's networking (HTTPRequest) for calling the Python backend
  
## Features different NPCs with different personalities

Erik Stoneforge - cynical, superstitious, blunt

https://github.com/user-attachments/assets/a280b9c4-f63b-4edb-a810-1b356a0022f2

Valerius Van Der Haut - Poetic, rambly, sophisticated, condescending

https://github.com/user-attachments/assets/2edc9d7c-ed9e-4a2c-9b71-e240255da2cd

