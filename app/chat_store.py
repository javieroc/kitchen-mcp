"""Supabase persistence for chat threads and messages."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from supabase import Client

from .db import build_supabase_client


class ChatStore:
    """Thin data access layer for chat entities."""

    def __init__(self, access_token: str):
        self.client: Client = build_supabase_client(access_token)

    def create_thread(self, user_id: str, title: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"owner_id": user_id}
        if title:
            payload["title"] = title.strip()

        response = self.client.table("chat_threads").insert(payload).execute()
        if not response.data:
            raise RuntimeError("Could not create chat thread.")
        return response.data[0]

    def list_threads(self, user_id: str, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        end = offset + max(limit, 1) - 1
        response = (
            self.client.table("chat_threads")
            .select("*")
            .eq("owner_id", user_id)
            .is_("archived_at", "null")
            .order("last_message_at", desc=True)
            .range(offset, end)
            .execute()
        )
        return response.data or []

    def get_thread(self, thread_id: UUID, user_id: str) -> dict[str, Any] | None:
        response = (
            self.client.table("chat_threads")
            .select("*")
            .eq("id", str(thread_id))
            .eq("owner_id", user_id)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        return rows[0] if rows else None

    def get_messages(self, thread_id: UUID, user_id: str) -> list[dict[str, Any]]:
        response = (
            self.client.table("chat_messages")
            .select("*")
            .eq("thread_id", str(thread_id))
            .eq("owner_id", user_id)
            .order("sequence_no")
            .execute()
        )
        return response.data or []

    def get_messages_page(
        self,
        thread_id: UUID,
        user_id: str,
        limit: int,
        before: int | None = None,
    ) -> tuple[list[dict[str, Any]], bool]:
        """Return a page of messages and whether older messages still exist.

        Fetches ``limit + 1`` rows descending so we can detect ``has_more``
        without a separate count query, then reverses to chronological order.

        Args:
            before: Exclusive upper bound on ``sequence_no``. When supplied,
                    only messages older than this cursor are returned.

        Returns:
            A tuple of (messages in chronological order, has_more).
        """
        query = (
            self.client.table("chat_messages")
            .select("*")
            .eq("thread_id", str(thread_id))
            .eq("owner_id", user_id)
            .order("sequence_no", desc=True)
            .limit(limit + 1)
        )
        if before is not None:
            query = query.lt("sequence_no", before)

        rows = query.execute().data or []

        has_more = len(rows) > limit
        if has_more:
            rows = rows[:limit]

        rows.reverse()  # chronological order for the client
        return rows, has_more

    def add_message(
        self,
        *,
        thread_id: UUID,
        user_id: str,
        role: str,
        content: str,
        tools_used: list[str] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "thread_id": str(thread_id),
            "owner_id": user_id,
            "role": role,
            "content": content,
        }
        if tools_used:
            payload["tools_used"] = tools_used

        response = self.client.table("chat_messages").insert(payload).execute()
        if not response.data:
            raise RuntimeError("Could not persist chat message.")
        return response.data[0]
