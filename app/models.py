"""Request/response models for the API."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming prompt payload from the mobile client."""

    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """API response for chat completions."""

    user_id: str
    reply: str
    tools_used: list[str] = Field(default_factory=list)
