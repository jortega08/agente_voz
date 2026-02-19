import uuid
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.core.database import get_db
from app.models.conversation import Conversation, ConversationMessage
from app.services.voice.stt import transcribe_audio
from app.services.voice.tts import synthesize_speech
from app.services.emotional.classifier import classify_emotion
from app.services.strategy.negotiation import NegotiationEngine
from app.services.personaplex.client import PersonaPlexClient

logger = structlog.get_logger()

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        self.active_connections.pop(session_id, None)

    async def send_json(self, session_id: str, data: dict):
        ws = self.active_connections.get(session_id)
        if ws:
            await ws.send_json(data)


manager = ConnectionManager()


@router.websocket("/conversation/{conversation_id}")
async def websocket_conversation(
    websocket: WebSocket,
    conversation_id: uuid.UUID,
):
    session_id = str(conversation_id)
    await manager.connect(websocket, session_id)

    logger.info("websocket_connected", conversation_id=session_id)

    try:
        while True:
            data = await websocket.receive_bytes()

            # 1. Speech to text
            transcript = await transcribe_audio(data)
            if not transcript:
                continue

            await manager.send_json(session_id, {
                "type": "transcription",
                "role": "user",
                "content": transcript,
            })

            # 2. Classify emotion
            emotion = await classify_emotion(transcript)
            await manager.send_json(session_id, {
                "type": "emotion",
                "emotion": emotion,
            })

            # 3. Generate agent response (placeholder for PersonaPlex integration)
            response_text = f"[Agent response to: {transcript}]"

            await manager.send_json(session_id, {
                "type": "transcription",
                "role": "agent",
                "content": response_text,
            })

            # 4. Text to speech
            audio_bytes = await synthesize_speech(response_text)
            if audio_bytes:
                await websocket.send_bytes(audio_bytes)

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info("websocket_disconnected", conversation_id=session_id)
