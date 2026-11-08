# Simple AI Agent (Python + Ollama)

A minimal AI agent built from scratch with plain Python, to learn how agents work
before using frameworks like LangGraph.

## Features
- Chat with a local model (qwen2.5:3b) via Ollama
- Memory: conversation is saved to a JSON file and continued on the next run
- Tool use: the model decides when to call `get_time()` to get the real time

## How it works
1. User message is added to the conversation
2. The conversation is sent to the model
3. If the model asks for a tool, Python runs it and sends the result back
4. The model gives the final answer

See `example_conversation.json` for a sample conversation with a tool call.

## Run
uv sync
uv run conversation_save_history_tool.py

Type `exit` to quit.

## Requirements
- Python 3.10+
- Ollama with the `qwen2.5:3b` model (`ollama pull qwen2.5:3b`)