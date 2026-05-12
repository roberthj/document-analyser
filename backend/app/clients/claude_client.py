import os
import anthropic
from typing import Any
from anthropic.types import TextBlockParam, ToolChoiceToolParam, CacheControlEphemeralParam, MessageParam, ToolParam

_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
_llm_model = os.environ["LLM_MODEL"]

# Use tool to make claude return structured data
def run_extraction(user_prompt: str, system_prompt: str, tool_schema: dict) -> Any:
    response = _client.messages.create(
        model=_llm_model,
        max_tokens=4096,
        system=[TextBlockParam(type="text", text=system_prompt, cache_control=CacheControlEphemeralParam(type="ephemeral"))],   # Caching the system prompt
        tools=[ToolParam(**tool_schema)],
        tool_choice=ToolChoiceToolParam(type="tool", name=tool_schema["name"]),
        messages=[MessageParam(role="user", content=user_prompt)],
    )
    tool_block = next((b for b in response.content if b.type == "tool_use"), None)  # Getting only the structured data

    if tool_block is None:
        raise ValueError("Claude did not return a tool use block")          #Will return 500 response. Could catch this and make friendlier response
    return tool_block.input
