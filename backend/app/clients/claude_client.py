import os
import anthropic

_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
_llm_model = os.environ["LLM_MODEL"]

# Use tool to make claude return structured data
def run_extraction(user_prompt: str, system_prompt: str, tool_schema: dict) -> dict:
    response = _client.messages.create(
        model=_llm_model,
        max_tokens=2048,
        system=system_prompt,
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": tool_schema["name"]},
        messages=[{"role": "user", "content": user_prompt}],
    )
    tool_block = next(b for b in response.content if b.type == "tool_use")      # Returns only the structured data (fype=tool_use)
    return tool_block.input
