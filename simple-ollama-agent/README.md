# Simple AI Agent (Python + Ollama)

A minimal AI agent built from scratch with plain Python, to learn how agents
work before using frameworks like LangChain and LangGraph.

## Steps

| File | What it adds |
|---|---|
| `01-time_agent.py` | Chat with a local model, memory in a JSON file, a tool without input (`get_time`) |
| `02-tool-with-arguments.py` | Tools with input (`check_age`, `divide`), several tools at once, error handling inside a tool, a system prompt |

## How it works

1. The user's message is added to the conversation (a list of messages).
2. The whole conversation is sent to the model.
3. If the model asks for a tool, Python runs it and adds the result to the conversation.
4. The conversation is sent again, and the model gives the final answer.
5. The conversation is saved to a JSON file, so the next run continues where this one stopped.

The model decides *when* to use a tool. For example, "what time is it?" calls
`get_time`, but "what is Python?" calls nothing.

## Example conversations

See the `examples/` folder:

- `01_example_conversation.json`: a tool call, a normal question, and a follow-up that shows memory
- `02_example_conversation.json`: a tool with input, a tool error handled safely, and a normal question

## Run

Install Ollama and pull the model:

    ollama pull qwen2.5:3b

Then, from this folder:

    uv sync
    uv run 02-tool-with-arguments.py

Type `exit` to quit. The conversation is saved to `02_conversation.json`.

## Notes

- Small local models are not always reliable. With several questions in one
  message, the model may skip a tool, so a system prompt asks it to answer all parts.
- The Ollama client uses `trust_env=False` so a system proxy or VPN does not
  block the connection to the local Ollama server.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/) with the `qwen2.5:3b` model