"""FastAPI application factory for the Kitchen Orchestrator API."""

import asyncio
import logging
import os
import socket
from contextlib import asynccontextmanager
from urllib.parse import urlparse

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .agent import process_chat_prompt
from .auth import AuthenticatedUser, get_current_user
from .mcp_client import MCPKitchenClient
from .models import ChatRequest, ChatResponse
from .routers import chats, recipes

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# MCP connectivity probe (run at startup)
# ---------------------------------------------------------------------------


async def _log_mcp_connectivity_probe(server_url: str) -> None:
    parsed = urlparse(server_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if not host:
        logger.warning("MCP probe skipped: could not parse host from %s", server_url)
        return

    try:
        addrinfo = await asyncio.get_running_loop().getaddrinfo(
            host, port, type=socket.SOCK_STREAM
        )
        addresses = sorted({item[4][0] for item in addrinfo})
        logger.warning("MCP host %s resolved to %s", host, addresses)
    except Exception as exc:
        logger.warning("MCP DNS resolution failed for %s:%s: %s", host, port, exc)

    writer = None
    try:
        _, writer = await asyncio.open_connection(host, port)
        logger.warning("MCP TCP connection succeeded to %s:%s", host, port)
    except Exception as exc:
        logger.warning("MCP TCP connection failed to %s:%s: %s", host, port, exc)
    finally:
        if writer is not None:
            writer.close()
            await writer.wait_closed()

    health_url = parsed._replace(path="/health", params="", query="", fragment="").geturl()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(health_url)
        logger.warning("MCP health probe %s returned %s", health_url, response.status_code)
    except Exception as exc:
        logger.warning("MCP health probe failed for %s: %s", health_url, exc)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    mcp_client = MCPKitchenClient()
    app.state.mcp_client = mcp_client
    logger.warning("Using MCP_SERVER_URL=%s", mcp_client.server_url)
    await _log_mcp_connectivity_probe(mcp_client.server_url)
    yield


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------


app = FastAPI(title="Kitchen Orchestrator API", version="0.1.0", lifespan=lifespan)

app.include_router(chats.router)
app.include_router(recipes.router)


# ---------------------------------------------------------------------------
# Root / health / stateless chat
# ---------------------------------------------------------------------------


@app.get("/")
async def root():
    """Welcome endpoint."""
    return JSONResponse(
        {"message": "Kitchen Orchestrator API", "version": "0.1.0", "status": "running"}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    mcp_ok = await app.state.mcp_client.health_check()
    return JSONResponse(
        {
            "status": "healthy" if mcp_ok else "degraded",
            "service": "kitchen-orchestrator",
            "mcp_reachable": mcp_ok,
        }
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Stateless chat endpoint (no thread persistence)."""
    try:
        result = await process_chat_prompt(
            prompt=payload.message,
            user_id=user.user_id,
            mcp_client=app.state.mcp_client,
        )
        return ChatResponse(
            user_id=user.user_id,
            reply=result.reply,
            tools_used=result.tools_used,
        )
    except Exception as exc:
        logger.exception("Failed to process chat prompt")
        raise HTTPException(status_code=500, detail="Failed to process chat prompt.") from exc


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8001"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
