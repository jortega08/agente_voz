"""
Text-to-Speech service using Coqui TTS.

Converts text responses to audio for playback to the user.
"""

import io
import structlog

logger = structlog.get_logger()

_synthesizer = None


def _get_synthesizer():
    global _synthesizer
    if _synthesizer is None:
        try:
            from TTS.api import TTS
            from app.config import get_settings

            settings = get_settings()
            _synthesizer = TTS(model_name=settings.tts_model_name)
            logger.info("tts_model_loaded", model=settings.tts_model_name)
        except Exception as e:
            logger.warning("tts_model_not_available", error=str(e))
    return _synthesizer


async def synthesize_speech(text: str) -> bytes | None:
    """
    Convert text to speech audio.

    Args:
        text: The text to synthesize.

    Returns:
        Audio bytes (WAV format) or None if synthesis fails.
    """
    synthesizer = _get_synthesizer()
    if synthesizer is None:
        logger.warning("tts_skipped_no_model")
        return None

    try:
        wav = synthesizer.tts(text=text)

        buffer = io.BytesIO()
        import soundfile as sf
        sf.write(buffer, wav, samplerate=22050, format="WAV")
        audio_bytes = buffer.getvalue()

        logger.info("tts_synthesized", text_length=len(text), audio_size=len(audio_bytes))
        return audio_bytes

    except Exception as e:
        logger.error("tts_error", error=str(e))
        return None
