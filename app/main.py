"""FastAPI routes for Kitchen Orchestration."""
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .agent import process_chat_prompt
from .auth import AuthenticatedUser, get_current_user
from .mcp_client import MCPKitchenClient
from .models import ChatRequest, ChatResponse

app = FastAPI(title="Kitchen Orchestrator API", version="0.1.0")
mcp_client = MCPKitchenClient()


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
    return JSONResponse({
        "status": "healthy",
        "service": "kitchen-orchestrator"
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
        raise HTTPException(status_code=500, detail=f"Failed to process chat prompt: {exc}") from exc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
