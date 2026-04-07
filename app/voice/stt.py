"""Speech-to-Text via Groq Whisper (free tier, OpenAI-compatible)."""

import os

from groq import AsyncGroq

# Groq Whisper supports: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm (max 25 MB)
_SUPPORTED_MIME_TYPES = {
    "audio/flac",
    "audio/mpeg",
    "audio/mp4",
    "audio/x-m4a",
    "audio/ogg",
    "audio/wav",
    "audio/webm",
    "audio/x-wav",
    "video/mp4",
    "video/mpeg",
    "video/webm",
}


def _get_client() -> AsyncGroq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set.")
    return AsyncGroq(api_key=api_key)


async def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    content_type: str,
    *,
    language: str | None = None,
) -> str:
    """Transcribe audio bytes to text using Groq Whisper.

    Args:
        audio_bytes: Raw audio file contents.
        filename: Original filename (used by Groq for format detection).
        content_type: MIME type of the audio (e.g. ``audio/webm``).
        language: Optional BCP-47 language code (e.g. ``"en"``). If omitted,
            Whisper auto-detects the language.

    Returns:
        Transcribed text string.

    Raises:
        RuntimeError: If GROQ_API_KEY is missing.
        ValueError: If the content_type is not a recognised audio format.
    """
    if content_type not in _SUPPORTED_MIME_TYPES:
        raise ValueError(
            f"Unsupported audio format '{content_type}'. "
            f"Supported types: {', '.join(sorted(_SUPPORTED_MIME_TYPES))}"
        )

    client = _get_client()
    kwargs: dict = {
        "file": (filename, audio_bytes, content_type),
        "model": "whisper-large-v3",
        "response_format": "text",
    }
    if language:
        kwargs["language"] = language

    transcription = await client.audio.transcriptions.create(**kwargs)
    # When response_format="text", the SDK returns a plain str.
    return transcription if isinstance(transcription, str) else transcription.text
