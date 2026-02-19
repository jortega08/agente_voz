import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.conversation import Conversation
from app.models.debtor import Debtor
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationDetail,
)

router = APIRouter()


@router.post("/", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    data: ConversationCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Debtor).where(Debtor.id == data.debtor_id))
    debtor = result.scalar_one_or_none()
    if not debtor:
        raise HTTPException(status_code=404, detail="Debtor not found")

    conversation = Conversation(**data.model_dump())
    db.add(conversation)
    await db.flush()
    await db.refresh(conversation)
    return conversation


@router.get("/", response_model=list[ConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    debtor_id: uuid.UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Conversation)
    if status:
        query = query.where(Conversation.status == status)
    if debtor_id:
        query = query.where(Conversation.debtor_id == debtor_id)
    query = query.order_by(Conversation.started_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .options(selectinload(Conversation.messages))
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
