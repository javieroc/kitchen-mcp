"""Chat thread and message endpoints."""

import base64
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status

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
    VoiceMessageResponse,
)
from ..voice.stt import transcribe_audio
from ..voice.tts import synthesize_speech

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

        recent_rows, _ = store.get_messages_page(
            thread_id=chat_id, user_id=user.user_id, limit=6
        )
        conversation_history = [
            {"role": row["role"], "content": row["content"]} for row in recent_rows
        ]

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
            conversation_history=conversation_history,
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


@router.post("/{chat_id}/messages/voice", response_model=VoiceMessageResponse)
async def send_voice_message(
    chat_id: UUID,
    audio: UploadFile = File(..., description="Audio file (mp3, wav, webm, ogg, m4a, flac — max 25 MB)"),
    tts: bool = Query(
        default=False,
        description="If true, synthesize the assistant reply to speech and include base64 MP3 in the response.",
    ),
    language: str | None = Query(
        default=None,
        description="Optional BCP-47 language code for STT (e.g. 'en', 'es'). Omit for auto-detection.",
    ),
    user: AuthenticatedUser = Depends(get_current_user),
    mcp_client: MCPKitchenClient = Depends(_get_mcp_client),
):
    """Accept an audio file, transcribe it, run the chat agent, and return the response.

    **Flow:**
    1. Audio → Groq Whisper (STT) → transcription text
    2. Transcription → existing chat agent → assistant reply
    3. Both messages persisted to the chat thread
    4. (Optional, `?tts=true`) Reply → ElevenLabs TTS → base64 MP3 in response

    **Supported audio formats:** flac, mp3, mp4, m4a, ogg, wav, webm (max 25 MB).
    """
    try:
        audio_bytes = await audio.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to read uploaded audio file.") from exc

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file exceeds the 25 MB limit.")

    # 1. Speech → Text
    try:
        transcription = await transcribe_audio(
            audio_bytes=audio_bytes,
            filename=audio.filename or "audio",
            content_type=audio.content_type or "audio/webm",
            language=language,
        )
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.exception("STT service misconfigured")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("STT transcription failed")
        raise HTTPException(status_code=502, detail="Speech-to-text transcription failed.") from exc

    if not transcription.strip():
        raise HTTPException(status_code=422, detail="No speech detected in the audio file.")

    # 2. Chat agent (reuses the same logic as the text endpoint)
    try:
        store = _get_store(user)
        thread = store.get_thread(thread_id=chat_id, user_id=user.user_id)
        if not thread:
            raise HTTPException(status_code=404, detail="Chat not found.")

        recent_rows, _ = store.get_messages_page(
            thread_id=chat_id, user_id=user.user_id, limit=6
        )
        conversation_history = [
            {"role": row["role"], "content": row["content"]} for row in recent_rows
        ]

        user_message = store.add_message(
            thread_id=chat_id,
            user_id=user.user_id,
            role="user",
            content=transcription,
        )
        result = await process_chat_prompt(
            prompt=transcription,
            user_id=user.user_id,
            mcp_client=mcp_client,
            conversation_history=conversation_history,
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
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to process voice chat message")
        raise HTTPException(status_code=500, detail="Failed to process chat message.") from exc

    # 3. (Optional) Text → Speech
    audio_base64: str | None = None
    audio_mime_type: str | None = None
    if tts:
        try:
            tts_bytes = await synthesize_speech(result.reply)
            audio_base64 = base64.b64encode(tts_bytes).decode()
            audio_mime_type = "audio/mpeg"
        except RuntimeError as exc:
            logger.warning("TTS service misconfigured, skipping: %s", exc)
        except Exception as exc:
            logger.warning("TTS synthesis failed, skipping: %s", exc)

    return VoiceMessageResponse(
        transcription=transcription,
        thread=_to_chat_thread(refreshed_thread),
        user_message=_to_chat_message(user_message),
        assistant_message=_to_chat_message(assistant_message),
        audio_base64=audio_base64,
        audio_mime_type=audio_mime_type,
    )
