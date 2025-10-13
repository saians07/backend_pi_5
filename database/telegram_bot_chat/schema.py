from datetime import datetime
from typing import (
    Optional
)
from sqlalchemy import (
    String,
    BigInteger,
    Boolean,
    DateTime,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from database.base import Base

class BotChatHistory(Base):
    __tablename__ = 'telegram_bot_chat_history'

    id: Mapped[int] = mapped_column(primary_key=True)
    update_id: Mapped[int] = mapped_column(BigInteger)
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    created_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class BotUserMapping(Base):
    __tablename__ = 'telegram_bot_user_mapping'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(String(100))
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class BotUserSummary(Base):
    __tablename__ = 'telegram_bot_user_summary'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column(String(100))
    last_chat_datetime: Mapped[datetime] = mapped_column(DateTime)
    last_chat_summary: Mapped[str] = mapped_column(String(2000))
