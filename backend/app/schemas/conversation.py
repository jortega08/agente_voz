import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    debtor_id: uuid.UUID
    strategy: str = Field(
        default="empathetic",
        pattern="^(empathetic|firm|informative|urgent)$",
    )


class ConversationResponse(BaseModel):
    id: uuid.UUID
    debtor_id: uuid.UUID
    status: str
    strategy: str
    emotional_state_detected: str | None
    negotiation_result: str | None
    offered_amount: float | None
    accepted_amount: float | None
    duration_seconds: int | None
    started_at: datetime
    ended_at: datetime | None

    model_config = {"from_attributes": True}


class ConversationMessageResponse(BaseModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    emotional_tone: str | None
    confidence: float | None
    timestamp: datetime

    model_config = {"from_attributes": True}


class ConversationDetail(ConversationResponse):
    messages: list[ConversationMessageResponse] = []


class MetricsSummary(BaseModel):
    total_conversations: int
    completed_conversations: int
    avg_duration_seconds: float | None
    acceptance_rate: float | None
    emotional_distribution: dict[str, int]
    strategy_effectiveness: dict[str, float]
