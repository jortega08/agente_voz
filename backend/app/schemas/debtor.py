import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DebtorCreate(BaseModel):
    external_id: str | None = None
    name: str = Field(min_length=1, max_length=200)
    original_amount: float = Field(gt=0)
    negotiable_amount: float = Field(gt=0)
    days_past_due: int = Field(ge=0)
    risk_profile: str = Field(default="medium", pattern="^(low|medium|high)$")
    emotional_profile: str | None = Field(
        default=None,
        pattern="^(cooperative|defensive|aggressive|evasive|anxious)$",
    )
    notes: str | None = None


class DebtorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    original_amount: float | None = Field(default=None, gt=0)
    negotiable_amount: float | None = Field(default=None, gt=0)
    days_past_due: int | None = Field(default=None, ge=0)
    risk_profile: str | None = Field(
        default=None, pattern="^(low|medium|high)$"
    )
    emotional_profile: str | None = Field(
        default=None,
        pattern="^(cooperative|defensive|aggressive|evasive|anxious)$",
    )
    notes: str | None = None


class DebtorResponse(BaseModel):
    id: uuid.UUID
    external_id: str | None
    name: str
    original_amount: float
    negotiable_amount: float
    days_past_due: int
    risk_profile: str
    emotional_profile: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
