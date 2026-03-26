"""Request/response models for the API."""

from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming prompt payload from the mobile client."""

    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """API response for chat completions."""

    user_id: str
    reply: str
    tools_used: list[str] = Field(default_factory=list)


class CreateChatRequest(BaseModel):
    """Payload to create a new chat thread."""

    title: str | None = Field(default=None, max_length=200)


class SendMessageRequest(BaseModel):
    """Payload to append a user message in a chat thread."""

    message: str = Field(..., min_length=1, max_length=2000)


class ChatMessage(BaseModel):
    """A single message inside a chat thread."""

    id: str
    role: str
    content: str
    sequence_no: int
    created_at: datetime
    tools_used: list[str] = Field(default_factory=list)


class ChatThread(BaseModel):
    """A chat thread owned by one user."""

    id: str
    owner_id: str
    title: str | None = None
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime
    archived_at: datetime | None = None


class ChatThreadWithMessages(BaseModel):
    """Chat thread with full message history."""

    thread: ChatThread
    messages: list[ChatMessage] = Field(default_factory=list)


class SendMessageResponse(BaseModel):
    """Response after appending user + assistant turn."""

    thread: ChatThread
    user_message: ChatMessage
    assistant_message: ChatMessage
