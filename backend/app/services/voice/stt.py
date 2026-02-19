"""
Speech-to-Text service using OpenAI Whisper API.

Converts raw audio bytes to text transcription.
"""

import io
import wave
import structlog
from openai import AsyncOpenAI

from app.config import get_settings

logger = structlog.get_logger()


def _get_client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.openai_api_key)


def _wrap_pcm_as_wav(audio_bytes: bytes, sample_rate: int = 16000) -> io.BytesIO:
    """Wrap raw 16-bit PCM bytes into a WAV container for the OpenAI API."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)
    buffer.seek(0)
    buffer.name = "audio.wav"
    return buffer


async def transcribe_audio(audio_bytes: bytes) -> str | None:
    """
    Transcribe audio bytes to text using OpenAI Whisper API.

    Args:
        audio_bytes: Raw audio data (16kHz, mono, 16-bit PCM).

    Returns:
        Transcribed text or None if transcription fails.
    """
    if not audio_bytes:
        return None

    settings = get_settings()
    client = _get_client()

    try:
        wav_buffer = _wrap_pcm_as_wav(audio_bytes)
        response = await client.audio.transcriptions.create(
            model=settings.openai_stt_model,
            file=wav_buffer,
            language="es",
        )
        text = response.text.strip()
        if text:
            logger.info("stt_transcription", text=text[:100])
        return text if text else None

    except Exception as e:
        logger.error("stt_error", error=str(e))
        return None
