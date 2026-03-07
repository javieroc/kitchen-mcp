"""FastAPI routes for Kitchen Orchestration."""
import logging
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .agent import process_chat_prompt
from .auth import AuthenticatedUser, get_current_user
from .mcp_client import MCPKitchenClient
from .models import ChatRequest, ChatResponse

app = FastAPI(title="Kitchen Orchestrator API", version="0.1.0")
mcp_client = MCPKitchenClient()
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    """Welcome endpoint."""
    return JSONResponse({
        "message": "Kitchen Orchestrator API",
        "version": "0.1.0",
        "status": "running"
    })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    mcp_ok = await mcp_client.health_check()
    status = "healthy" if mcp_ok else "degraded"
    return JSONResponse({
        "status": status,
        "service": "kitchen-orchestrator",
        "mcp_reachable": mcp_ok,
    })


@app.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Process a chat prompt from the mobile app."""
    try:
        result = await process_chat_prompt(
            prompt=payload.message,
            user_id=user.user_id,
            mcp_client=mcp_client,
        )
        return ChatResponse(
            user_id=user.user_id,
            reply=result.reply,
            tools_used=result.tools_used,
        )
    except Exception as exc:
        logger.exception("Failed to process chat prompt")
        raise HTTPException(status_code=500, detail="Failed to process chat prompt.") from exc


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
