"""Supabase persistence for chat threads and messages."""

from __future__ import annotations

import os
from typing import Any
from uuid import UUID

from supabase import Client, create_client


def _build_supabase_data_client(access_token: str) -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY (or service role key) must be configured.")

    client = create_client(url, key)
    client.postgrest.auth(access_token)
    return client


class ChatStore:
    """Thin data access layer for chat entities."""

    def __init__(self, access_token: str):
        self.client = _build_supabase_data_client(access_token)

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
