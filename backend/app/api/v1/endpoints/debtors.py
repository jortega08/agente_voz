import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.debtor import Debtor
from app.schemas.debtor import DebtorCreate, DebtorUpdate, DebtorResponse

router = APIRouter()


@router.post("/", response_model=DebtorResponse, status_code=201)
async def create_debtor(data: DebtorCreate, db: AsyncSession = Depends(get_db)):
    debtor = Debtor(**data.model_dump())
    db.add(debtor)
    await db.flush()
    await db.refresh(debtor)
    return debtor


@router.get("/", response_model=list[DebtorResponse])
async def list_debtors(
    skip: int = 0,
    limit: int = 50,
    risk_profile: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Debtor)
    if risk_profile:
        query = query.where(Debtor.risk_profile == risk_profile)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{debtor_id}", response_model=DebtorResponse)
async def get_debtor(debtor_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Debtor).where(Debtor.id == debtor_id))
    debtor = result.scalar_one_or_none()
    if not debtor:
        raise HTTPException(status_code=404, detail="Debtor not found")
    return debtor


@router.patch("/{debtor_id}", response_model=DebtorResponse)
async def update_debtor(
    debtor_id: uuid.UUID,
    data: DebtorUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Debtor).where(Debtor.id == debtor_id))
    debtor = result.scalar_one_or_none()
    if not debtor:
        raise HTTPException(status_code=404, detail="Debtor not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(debtor, field, value)

    await db.flush()
    await db.refresh(debtor)
    return debtor


@router.delete("/{debtor_id}", status_code=204)
async def delete_debtor(debtor_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Debtor).where(Debtor.id == debtor_id))
    debtor = result.scalar_one_or_none()
    if not debtor:
        raise HTTPException(status_code=404, detail="Debtor not found")
    await db.delete(debtor)
