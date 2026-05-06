from datetime import datetime, timezone
from sqlalchemy import Identity, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

class BaseModel(DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now)