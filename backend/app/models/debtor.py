import uuid
from datetime import datetime

from sqlalchemy import String, Float, Integer, DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Debtor(Base):
    __tablename__ = "debtors"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    external_id: Mapped[str | None] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(200))
    original_amount: Mapped[float] = mapped_column(Float)
    negotiable_amount: Mapped[float] = mapped_column(Float)
    days_past_due: Mapped[int] = mapped_column(Integer)
    risk_profile: Mapped[str] = mapped_column(
        String(50), default="medium"
    )  # low, medium, high
    emotional_profile: Mapped[str | None] = mapped_column(
        String(50)
    )  # cooperative, defensive, aggressive, evasive, anxious
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="debtor", cascade="all, delete-orphan"
    )
