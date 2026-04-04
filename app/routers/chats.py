"""Chat thread and message endpoints."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from ..agent import process_chat_prompt
from ..auth import AuthenticatedUser, get_current_user
from ..chat_store import ChatStore
from ..mcp_client import MCPKitchenClient
from ..models import (
    ChatMessage,
    ChatMessagesPage,
    ChatThread,
    ChatThreadWithMessages,
    CreateChatRequest,
    SendMessageRequest,
    SendMessageResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chats", tags=["chats"])


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_mcp_client(request: Request) -> MCPKitchenClient:
    return request.app.state.mcp_client


def _get_store(user: AuthenticatedUser) -> ChatStore:
    return ChatStore(user.access_token)


def _to_chat_thread(row: dict) -> ChatThread:
    return ChatThread.model_validate(row)


def _to_chat_message(row: dict) -> ChatMessage:
    return ChatMessage(
        id=row["id"],
        role=row["role"],
        content=row["content"],
        sequence_no=row["sequence_no"],
        created_at=row["created_at"],
        tools_used=row.get("tools_used") or [],
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("", response_model=ChatThread, status_code=status.HTTP_201_CREATED)
async def create_chat(
    payload: CreateChatRequest,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Create a new chat thread for the authenticated user."""
    try:
        store = _get_store(user)
        thread = store.create_thread(user_id=user.user_id, title=payload.title)
        return _to_chat_thread(thread)
    except Exception as exc:
        logger.exception("Failed to create chat thread")
        raise HTTPException(status_code=500, detail="Failed to create chat thread.") from exc


@router.get("", response_model=list[ChatThread])
async def list_chats(
    user: AuthenticatedUser = Depends(get_current_user),
):
    """List chat threads for the authenticated user."""
    try:
        store = _get_store(user)
        rows = store.list_threads(user_id=user.user_id)
        return [_to_chat_thread(row) for row in rows]
    except Exception as exc:
        logger.exception("Failed to list chat threads")
        raise HTTPException(status_code=500, detail="Failed to list chats.") from exc


@router.get("/{chat_id}", response_model=ChatThread)
async def get_chat(
    chat_id: UUID,
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Fetch thread metadata. Use GET /chats/{chat_id}/messages for messages."""
    try:
        store = _get_store(user)
        thread = store.get_thread(thread_id=chat_id, user_id=user.user_id)
        if not thread:
            raise HTTPException(status_code=404, detail="Chat not found.")
        return _to_chat_thread(thread)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to fetch chat thread")
        raise HTTPException(status_code=500, detail="Failed to fetch chat.") from exc


@router.get("/{chat_id}/messages", response_model=ChatMessagesPage)
async def get_chat_messages(
    chat_id: UUID,
    limit: int = Query(default=20, ge=1, le=100, description="Number of messages to return"),
    before: int | None = Query(
        default=None,
        description="Cursor: fetch messages with sequence_no older than this value. Omit to get the latest messages.",
    ),
    user: AuthenticatedUser = Depends(get_current_user),
):
    """Return a cursor-paginated page of messages (newest-first within each page is server-side, returned in chronological order).

    **How to paginate:**
    1. Call without `before` to get the latest `limit` messages.
    2. If `has_more` is `true`, call again with `before=next_cursor` to load older messages.
    3. Repeat until `has_more` is `false`.
    """
    try:
        store = _get_store(user)
        thread = store.get_thread(thread_id=chat_id, user_id=user.user_id)
        if not thread:
            raise HTTPException(status_code=404, detail="Chat not found.")

        rows, has_more = store.get_messages_page(
            thread_id=chat_id,
            user_id=user.user_id,
            limit=limit,
            before=before,
        )
        messages = [_to_chat_message(row) for row in rows]
        next_cursor = messages[0].sequence_no if (has_more and messages) else None
        return ChatMessagesPage(messages=messages, has_more=has_more, next_cursor=next_cursor)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to fetch chat messages")
        raise HTTPException(status_code=500, detail="Failed to fetch messages.") from exc


@router.post("/{chat_id}/messages", response_model=SendMessageResponse)
async def send_chat_message(
    chat_id: UUID,
    payload: SendMessageRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    mcp_client: MCPKitchenClient = Depends(_get_mcp_client),
):
    """Append user message, run agent, and persist assistant response."""
    try:
        store = _get_store(user)
        thread = store.get_thread(thread_id=chat_id, user_id=user.user_id)
        if not thread:
            raise HTTPException(status_code=404, detail="Chat not found.")

        user_message = store.add_message(
            thread_id=chat_id,
            user_id=user.user_id,
            role="user",
            content=payload.message,
        )
        result = await process_chat_prompt(
            prompt=payload.message,
            user_id=user.user_id,
            mcp_client=mcp_client,
        )
        assistant_message = store.add_message(
            thread_id=chat_id,
            user_id=user.user_id,
            role="assistant",
            content=result.reply,
            tools_used=result.tools_used,
        )
        refreshed_thread = store.get_thread(thread_id=chat_id, user_id=user.user_id)
        if not refreshed_thread:
            raise HTTPException(status_code=404, detail="Chat not found.")

        return SendMessageResponse(
            thread=_to_chat_thread(refreshed_thread),
            user_message=_to_chat_message(user_message),
            assistant_message=_to_chat_message(assistant_message),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to process chat message")
        raise HTTPException(status_code=500, detail="Failed to process chat message.") from exc
