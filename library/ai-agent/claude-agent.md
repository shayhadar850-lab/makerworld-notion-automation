# Skill: Claude AI Agent (Anthropic SDK)

## Overview
Build an AI agent using Claude via the Anthropic API with tool use capabilities.

## Tech Stack
- Language: Python 3.11+ or TypeScript/Node.js
- SDK: anthropic (Python) or @anthropic-ai/sdk (Node)
- Model: claude-sonnet-4-5-20250929 (default) or claude-opus-4-6
- Tools: Custom function tools
- State: Conversation history management

## Python Project Structure
```
agent/
├── src/
│   ├── agent.py          # Main agent loop
│   ├── tools/
│   │   ├── __init__.py
│   │   └── *.py          # Individual tool definitions
│   ├── prompts/
│   │   └── system.md     # System prompt
│   └── config.py
├── .env                  # ANTHROPIC_API_KEY=...
├── requirements.txt
└── main.py
```

## Setup Steps
1. `pip install anthropic python-dotenv`
2. Set `ANTHROPIC_API_KEY` in `.env`
3. Define tools as Python functions with docstrings
4. Create agent loop with conversation history
5. Implement tool execution and result handling

## Core Agent Pattern (Python)
```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "tool_name",
        "description": "What this tool does",
        "input_schema": {
            "type": "object",
            "properties": {
                "param": {"type": "string", "description": "..."}
            },
            "required": ["param"]
        }
    }
]

def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })

            messages.append({"role": "user", "content": tool_results})
```

## Best Practices
- Always include a clear system prompt
- Keep tool descriptions precise - Claude relies on them
- Handle tool errors gracefully and return error messages
- Set appropriate max_tokens for your use case
- Use streaming for long responses
- Log all tool calls for debugging

## Common Pitfalls
- Don't forget to append tool results back to messages
- Tool input_schema must be valid JSON Schema
- Model name must be exact - check current model IDs
- API key must not be committed to git

## Models (as of 2026)
- `claude-sonnet-4-5-20250929` - Default, fast and capable
- `claude-opus-4-6` - Most capable, slower
- `claude-haiku-4-5-20251001` - Fastest, cheapest

## References
- Docs: https://docs.anthropic.com/
- Tool Use: https://docs.anthropic.com/claude/docs/tool-use
