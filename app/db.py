"""Shared Supabase client factory."""

from __future__ import annotations

import os

from fastapi import Depends
from supabase import Client, create_client

from .auth import AuthenticatedUser, get_current_user


def build_supabase_client(access_token: str) -> Client:
    """Create a Supabase client authenticated with the user's access token.

    A new client is created per-request so Supabase RLS sees the correct
    ``auth.uid()`` for every query.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_ANON_KEY (or service role key) must be configured."
        )
    client = create_client(url, key)
    client.postgrest.auth(access_token)
    return client


def get_supabase_client(
    user: AuthenticatedUser = Depends(get_current_user),
) -> Client:
    """FastAPI dependency that returns a per-request, user-scoped Supabase client."""
    return build_supabase_client(user.access_token)
