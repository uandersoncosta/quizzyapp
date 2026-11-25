import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="profile"
    )