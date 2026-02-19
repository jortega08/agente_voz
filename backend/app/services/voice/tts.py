"""
Text-to-Speech service using OpenAI TTS API.

Converts text responses to audio (MP3) for playback to the user.
"""

import structlog
from openai import AsyncOpenAI

from app.config import get_settings

logger = structlog.get_logger()


def _get_client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.openai_api_key)


async def synthesize_speech(text: str) -> bytes | None:
    """
    Convert text to speech audio using OpenAI TTS API.

    Args:
        text: The text to synthesize.

    Returns:
        Audio bytes (MP3 format) or None if synthesis fails.
    """
    if not text:
        return None

    settings = get_settings()
    client = _get_client()

    try:
        response = await client.audio.speech.create(
            model=settings.openai_tts_model,
            voice=settings.openai_tts_voice,
            input=text,
            response_format="mp3",
        )
        audio_bytes = response.content
        logger.info("tts_synthesized", text_length=len(text), audio_size=len(audio_bytes))
        return audio_bytes

    except Exception as e:
        logger.error("tts_error", error=str(e))
        return None
