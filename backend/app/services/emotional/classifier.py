"""
Emotional state classifier for conversation text.

Analyzes user messages to detect emotional state and adapt
the agent's strategy accordingly.

Phase 1: Rule-based keyword classification.
Phase 2+: ML-based classifier with fine-tuned model.
"""

import re
import structlog

logger = structlog.get_logger()

EMOTION_KEYWORDS = {
    "aggressive": [
        "angry", "furious", "stop calling", "leave me alone", "harassment",
        "sue", "lawyer", "report", "scam", "fraud", "damn", "hell",
        "shut up", "ridiculous", "unacceptable",
    ],
    "anxious": [
        "worried", "scared", "afraid", "nervous", "panic", "can't sleep",
        "stress", "overwhelmed", "desperate", "help me", "don't know what to do",
        "losing", "bankruptcy",
    ],
    "cooperative": [
        "understand", "agree", "yes", "okay", "sure", "tell me more",
        "what are my options", "how can i", "willing", "let's",
        "payment plan", "work something out",
    ],
    "evasive": [
        "not now", "call back", "busy", "later", "don't have time",
        "wrong number", "not interested", "maybe", "i'll think about it",
        "send me something",
    ],
    "defensive": [
        "prove it", "not my debt", "already paid", "don't owe",
        "show me proof", "verify", "who are you", "how did you get",
        "rights", "not responsible",
    ],
}


async def classify_emotion(text: str) -> str:
    """
    Classify the emotional state of a text message.

    Args:
        text: The user's message text.

    Returns:
        Detected emotion: aggressive, anxious, cooperative, evasive, or defensive.
        Defaults to "cooperative" if no strong signal is detected.
    """
    text_lower = text.lower()
    scores = {}

    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[emotion] = score

    if not scores:
        return "cooperative"

    detected = max(scores, key=scores.get)
    logger.info(
        "emotion_classified",
        emotion=detected,
        scores=scores,
        text_preview=text[:80],
    )
    return detected
