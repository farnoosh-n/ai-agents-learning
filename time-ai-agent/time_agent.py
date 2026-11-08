"""
A simple AI agent built with plain Python and Ollama.

- Keeps conversation history in a JSON file (memory between runs)
- Chats with a local model (qwen2.5:3b)
- Uses a tool (get_time) when the model asks for it
"""

import json
import os
from datetime import datetime

import ollama

MODEL = "qwen2.5:3b"
FILE_NAME = "conversation.json"


def save_conversation(messages):
    """Save the conversation to a JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


def load_conversation():
    """Load the conversation from the JSON file."""
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def get_time():
    """Get the current time."""
    return datetime.now().strftime("%H:%M")


# ---- Start of program ----
if os.path.exists(FILE_NAME):
    data = load_conversation()   # continue the previous conversation
else:
    data = []                    # first run: start a new conversation

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    # 1. Add the user's message
    data.append({"role": "user", "content": user_input})

    # 2. Ask the model
    response = ollama.chat(model=MODEL, messages=data, tools=[get_time])
    tool_calls = response["message"].get("tool_calls")
    print("tool_calls:", tool_calls)

    # 3. If the model asked for a tool: run it and ask again
    if tool_calls:
        # The model's request: "please run get_time"
        data.append({"role": "assistant", "content": "",
                     "tool_calls": [{"function": {"name": "get_time", "arguments": {}}}]})
        # The tool result
        data.append({"role": "tool", "content": get_time(), "tool_name": "get_time"})
        # Ask again, now the model can see the result
        response = ollama.chat(model=MODEL, messages=data, tools=[get_time])

    # 4. Final answer
    answer = response["message"]["content"]
    data.append({"role": "assistant", "content": answer})
    print("Assistant:", answer)
    save_conversation(data)