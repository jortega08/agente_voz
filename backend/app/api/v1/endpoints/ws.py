import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
import structlog

from app.core.database import async_session
from app.models.conversation import Conversation, ConversationMessage
from app.services.voice.stt import transcribe_audio
from app.services.voice.tts import synthesize_speech
from app.services.emotional.classifier import classify_emotion
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
_personaplex = PersonaPlexClient()


@router.websocket("/conversation/{conversation_id}")
async def websocket_conversation(
    websocket: WebSocket,
    conversation_id: uuid.UUID,
):
    session_id = str(conversation_id)
    await manager.connect(websocket, session_id)
    logger.info("websocket_connected", conversation_id=session_id)

    conversation_history: list[dict] = []
    persona_config: dict | None = None

    # Load conversation context (debtor info + strategy) from DB
    async with async_session() as db:
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conv = result.scalar_one_or_none()
        if conv:
            debtor_result = await db.execute(
                select(conv.__class__).where(conv.__class__.id == conv.id)
            )
            persona_config = {"strategy": conv.strategy}

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
            if persona_config is not None:
                persona_config["emotional_state"] = emotion
            await manager.send_json(session_id, {
                "type": "emotion",
                "emotion": emotion,
            })

            # 3. Generate agent response via OpenAI GPT
            response_text = await _personaplex.generate_text_response(
                text_input=transcript,
                persona_config=persona_config,
                conversation_history=conversation_history,
            )

            # Update in-memory conversation history
            conversation_history.append({"role": "user", "content": transcript})
            conversation_history.append({"role": "assistant", "content": response_text})

            await manager.send_json(session_id, {
                "type": "transcription",
                "role": "agent",
                "content": response_text,
            })

            # 4. Persist messages to DB
            async with async_session() as db:
                db.add(ConversationMessage(
                    conversation_id=conversation_id,
                    role="user",
                    content=transcript,
                    emotional_tone=emotion,
                ))
                db.add(ConversationMessage(
                    conversation_id=conversation_id,
                    role="agent",
                    content=response_text,
                ))
                await db.commit()

            # 5. Text to speech
            audio_bytes = await synthesize_speech(response_text)
            if audio_bytes:
                await websocket.send_bytes(audio_bytes)

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        logger.info("websocket_disconnected", conversation_id=session_id)
