"""Async MCP client for kitchen tool calls."""

from __future__ import annotations

import os
from typing import Any

from fastmcp import Client


class MCPKitchenClient:
    """Thin wrapper over FastMCP client."""

    def __init__(self, server_url: str | None = None) -> None:
        self.server_url = server_url or os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")

    def _client(self) -> Client:
        return Client(self.server_url, timeout=30)

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Call a tool and return concatenated text content."""
        async with self._client() as client:
            result = await client.call_tool(tool_name, arguments, raise_on_error=False)

        if getattr(result, "isError", False):
            return f"Tool error in {tool_name}."

        parts: list[str] = []
        for content in result.content:
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
        return "\n".join(parts).strip() if parts else f"No textual output from tool {tool_name}."

    async def health_check(self) -> bool:
        """Return True if MCP server is reachable and can answer the connection tool."""
        try:
            response = await self.call_tool("check_connection", {})
        except Exception:
            return False
        return bool(response and "failed" not in response.lower())
