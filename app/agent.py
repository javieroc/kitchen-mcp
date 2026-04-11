"""Chat orchestration for kitchen assistant capabilities."""

from __future__ import annotations

from dataclasses import dataclass

from .llm_client import LLMClient
from .mcp_client import MCPKitchenClient


@dataclass
class AgentResult:
    """Agent response payload."""

    reply: str
    tools_used: list[str]


llm_client = LLMClient()


async def process_chat_prompt(
    prompt: str,
    user_id: str,
    mcp_client: MCPKitchenClient,
    conversation_history: list[dict] | None = None,
) -> AgentResult:
    """Run the kitchen agent: let the LLM decide which tools to call."""

    async def execute_tool(tool_name: str, args: dict) -> str:
        args["user_id"] = user_id
        return await mcp_client.call_tool(tool_name, args)

    reply, tools_used = await llm_client.run_agent_turn(
        user_prompt=prompt,
        conversation_history=conversation_history or [],
        tool_executor=execute_tool,
    )
    return AgentResult(reply=reply, tools_used=tools_used)
