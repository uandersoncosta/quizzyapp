import uuid
import enum

from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Uuid,
    Enum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class UserRole(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.FREE,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True
    )

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )