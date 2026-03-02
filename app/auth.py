"""Supabase token validation helpers for FastAPI."""

from __future__ import annotations

import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()


security = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    """Authenticated API principal."""

    user_id: str
    email: str | None = None
    access_token: str


def _build_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY (or service role key) must be configured.")
    return create_client(url, key)


supabase_auth_client = _build_supabase_client()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> AuthenticatedUser:
    """Validate bearer token with Supabase Auth and return principal."""
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    token = credentials.credentials
    try:
        user_response = supabase_auth_client.auth.get_user(token)
        user = user_response.user if user_response else None
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid auth token: {exc}",
        ) from exc

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth token",
        )

    return AuthenticatedUser(
        user_id=user.id,
        email=user.email,
        access_token=token,
    )
