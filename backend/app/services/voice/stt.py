"""
Speech-to-Text service using faster-whisper.

Converts raw audio bytes to text transcription.
"""

import io
import structlog
import numpy as np

logger = structlog.get_logger()

_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from faster_whisper import WhisperModel
            from app.config import get_settings

            settings = get_settings()
            _model = WhisperModel(
                settings.whisper_model_size,
                device=settings.whisper_device,
                compute_type="float16",
            )
            logger.info("whisper_model_loaded", size=settings.whisper_model_size)
        except Exception as e:
            logger.warning("whisper_model_not_available", error=str(e))
    return _model


async def transcribe_audio(audio_bytes: bytes) -> str | None:
    """
    Transcribe audio bytes to text.

    Args:
        audio_bytes: Raw audio data (16kHz, mono, 16-bit PCM).

    Returns:
        Transcribed text or None if transcription fails.
    """
    model = _get_model()
    if model is None:
        logger.warning("stt_skipped_no_model")
        return None

    try:
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
        audio_array /= 32768.0  # normalize to [-1, 1]

        segments, info = model.transcribe(audio_array, beam_size=5, language="en")
        text = " ".join(segment.text for segment in segments).strip()

        if text:
            logger.info("stt_transcription", text=text[:100], language=info.language)

        return text if text else None

    except Exception as e:
        logger.error("stt_error", error=str(e))
        return None
