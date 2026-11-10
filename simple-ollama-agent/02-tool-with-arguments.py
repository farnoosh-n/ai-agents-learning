"""
A simple AI agent built with plain Python and Ollama.

- Keeps conversation history in a JSON file (memory between runs)
- Chats with a local model (qwen2.5:3b)
- Uses tools (get_time, check_age, divide) when the model asks for them
"""

import json
import os
from datetime import datetime

import ollama

# trust_env=False: ignore system proxy settings and connect to Ollama directly
client = ollama.Client(host="http://127.0.0.1:11434", trust_env=False)

MODEL = "qwen2.5:3b"
FILE_NAME = "./examples/02_conversation.json"
SYSTEM_PROMPT = (
    "You are a helpful assistant. If the user asks several things, "
    "use every tool needed to answer ALL parts before replying."
)


def save_conversation(messages):
    """Save the conversation to a JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)


def load_conversation():
    """Load the conversation from the JSON file."""
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


# ---- Tools ----


def get_time():
    """Get the current time."""
    return datetime.now().strftime("%H:%M")


def check_age(age: int) -> str:
    """Check if a person is an adult.

    Args:
        age: The person's age in years
    """
    if age >= 18:
        return "adult"
    return "not adult"


def divide(a: int, b: int) -> str:
    """Divide a by b.

    Args:
        a: The number to divide
        b: The number to divide by
    """
    try:
        return str(a / b)
    except ZeroDivisionError:
        return "Error: cannot divide by zero"


TOOLS = [get_time, check_age, divide]

# ---- Start of program ----

if os.path.exists(FILE_NAME):
    data = load_conversation()  # continue the previous conversation
else:
    data = [{"role": "system", "content": SYSTEM_PROMPT}]  # first run

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break

    # 1. Add the user's message
    data.append({"role": "user", "content": user_input})

    # 2. Ask the model
    response = client.chat(model=MODEL, messages=data, tools=TOOLS)
    tool_calls = response["message"].get("tool_calls")
    print("tool_calls:", tool_calls)

    # 3. If the model asked for tools: run each one and ask again
    if tool_calls:
        for call in tool_calls:
            name = call["function"]["name"]  # which tool?
            args = call["function"]["arguments"]  # with what input?

            if name == "get_time":
                result = get_time()
            elif name == "check_age":
                result = check_age(args["age"])
            elif name == "divide":
                result = divide(args["a"], args["b"])
            else:
                result = f"Error: unknown tool {name}"

            # The model's request, then the tool's result
            data.append(
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{"function": {"name": name, "arguments": args}}],
                }
            )
            data.append({"role": "tool", "content": result, "tool_name": name})

        # Ask again, now the model can see the results
        response = client.chat(model=MODEL, messages=data, tools=TOOLS)

    # 4. Final answer
    answer = response["message"]["content"]
    data.append({"role": "assistant", "content": answer})
    print("Assistant:", answer)
    save_conversation(data)
