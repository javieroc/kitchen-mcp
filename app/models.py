"""Request/response models for the API."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

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


class ChatMessagesPage(BaseModel):
    """A page of messages for cursor-based pagination.

    To load older messages pass ``next_cursor`` as the ``before`` query
    parameter in the next request.
    """

    messages: list[ChatMessage]
    has_more: bool
    next_cursor: int | None = Field(
        default=None,
        description="sequence_no of the oldest message on this page. Pass as `before` to fetch the previous page.",
    )


class SendMessageResponse(BaseModel):
    """Response after appending user + assistant turn."""

    thread: ChatThread
    user_message: ChatMessage
    assistant_message: ChatMessage


class VoiceMessageResponse(BaseModel):
    """Response after processing a voice message.

    ``transcription`` contains the STT result so clients can display the
    recognised text alongside the assistant reply.  When the request includes
    ``?tts=true``, ``audio_base64`` holds the base64-encoded MP3 of the
    assistant response and ``audio_mime_type`` is ``"audio/mpeg"``.
    """

    transcription: str
    thread: ChatThread
    user_message: ChatMessage
    assistant_message: ChatMessage
    audio_base64: str | None = None
    audio_mime_type: str | None = None


# ---------------------------------------------------------------------------
# Recipe models
# ---------------------------------------------------------------------------


class Recipe(BaseModel):
    """A recipe owned by one user."""

    id: UUID
    name: str
    description: str | None = None
    category: str | None = None
    image_url: str | None = None
    owner_id: UUID
    created_at: datetime


class RecipeIngredientDetail(BaseModel):
    """A recipe–ingredient link enriched with ingredient metadata."""

    id: UUID
    recipe_id: UUID
    ingredient_id: UUID
    quantity_used: Decimal
    created_at: datetime
    ingredient_name: str
    unit_of_measure: str
    cost_per_unit: Decimal


class RecipeWithIngredients(BaseModel):
    """A recipe with its full ingredient list."""

    recipe: Recipe
    ingredients: list[RecipeIngredientDetail] = Field(default_factory=list)


class RecipeIngredientInput(BaseModel):
    """An ingredient entry used when creating a recipe.

    If the ingredient does not yet exist in your catalog it will be created
    automatically using ``unit_of_measure`` and ``cost_per_unit``.
    """

    name: str = Field(..., min_length=1, max_length=200)
    quantity_used: Decimal = Field(..., gt=0)
    unit_of_measure: str = Field(default="unit", description="Only used when auto-creating the ingredient. One of: g, kg, oz, lb, ml, L, tsp, tbsp, cup, unit")
    cost_per_unit: Decimal = Field(default=Decimal("0.00"), ge=0, description="Only used when auto-creating the ingredient")


class CreateRecipeRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=2000)
    ingredients: list[RecipeIngredientInput] = Field(default_factory=list)


class UpdateRecipeRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=2000)


class AddRecipeIngredientRequest(BaseModel):
    ingredient_id: UUID
    quantity_used: Decimal = Field(..., gt=0)


class UpdateRecipeIngredientRequest(BaseModel):
    quantity_used: Decimal = Field(..., gt=0)
