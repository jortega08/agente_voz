from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.conversation import Conversation
from app.schemas.conversation import MetricsSummary

router = APIRouter()


@router.get("/summary", response_model=MetricsSummary)
async def get_metrics_summary(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(Conversation.id)))
    completed = await db.scalar(
        select(func.count(Conversation.id)).where(Conversation.status == "completed")
    )
    avg_duration = await db.scalar(
        select(func.avg(Conversation.duration_seconds)).where(
            Conversation.duration_seconds.is_not(None)
        )
    )

    accepted = await db.scalar(
        select(func.count(Conversation.id)).where(
            Conversation.negotiation_result == "accepted"
        )
    )
    acceptance_rate = None
    if completed and completed > 0:
        acceptance_rate = accepted / completed

    emotional_result = await db.execute(
        select(
            Conversation.emotional_state_detected,
            func.count(Conversation.id),
        )
        .where(Conversation.emotional_state_detected.is_not(None))
        .group_by(Conversation.emotional_state_detected)
    )
    emotional_distribution = {
        row[0]: row[1] for row in emotional_result.all()
    }

    strategy_result = await db.execute(
        select(
            Conversation.strategy,
            func.avg(
                func.cast(
                    Conversation.negotiation_result == "accepted", type_=None
                )
            ),
        )
        .where(Conversation.status == "completed")
        .group_by(Conversation.strategy)
    )
    strategy_effectiveness = {
        row[0]: float(row[1]) if row[1] else 0.0
        for row in strategy_result.all()
    }

    return MetricsSummary(
        total_conversations=total or 0,
        completed_conversations=completed or 0,
        avg_duration_seconds=float(avg_duration) if avg_duration else None,
        acceptance_rate=acceptance_rate,
        emotional_distribution=emotional_distribution,
        strategy_effectiveness=strategy_effectiveness,
    )
