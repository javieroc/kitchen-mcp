"""Text-to-Speech via ElevenLabs (free tier: 10k chars/month)."""

import os

from elevenlabs.client import AsyncElevenLabs

_DEFAULT_VOICE_ID = "VjcrnUAQOh3B0DQu8iIm"
_DEFAULT_MODEL_ID = "eleven_multilingual_v2"
# Output: MP3 at 128 kbps — good balance of quality and payload size.
_OUTPUT_FORMAT = "mp3_44100_128"


def _get_client() -> AsyncElevenLabs:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY environment variable is not set.")
    return AsyncElevenLabs(api_key=api_key)


async def synthesize_speech(
    text: str,
    *,
    voice_id: str = _DEFAULT_VOICE_ID,
    model_id: str = _DEFAULT_MODEL_ID,
) -> bytes:
    """Convert text to speech and return raw MP3 bytes.

    Args:
        text: The text to synthesize (max ~10k chars/month on free tier).
        voice_id: ElevenLabs voice ID. Defaults to "Old British man".
        model_id: ElevenLabs model. Defaults to ``eleven_multilingual_v2``.

    Returns:
        Raw MP3 audio bytes.

    Raises:
        RuntimeError: If ELEVENLABS_API_KEY is missing.
    """
    client = _get_client()
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format=_OUTPUT_FORMAT,
    )
    return b"".join([chunk async for chunk in audio_stream])
