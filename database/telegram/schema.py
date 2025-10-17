# pylint: disable=C0114, R0903, E1102
from datetime import datetime
from typing import (
    Optional
)
from sqlalchemy import (
    ForeignKey,
    String,
    BigInteger,
    Integer,
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
    """Model to handle Chat History"""
    __tablename__ = 'telegram_bot_chat_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    update_id: Mapped[int] = mapped_column(BigInteger)
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('telegram_bot_user.id'))
    role: Mapped[str] = mapped_column(String(20))
    created_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class BotUserMapping(Base):
    """Model to handle User Mapping"""
    __tablename__ = 'telegram_bot_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_tele_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_name: Mapped[str] = mapped_column(String(100))
    is_allowed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class BotUserSummary(Base):
    """Model to handle User Summary"""
    __tablename__ = 'telegram_bot_user_summary'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('telegram_bot_user.id'))
    user_name: Mapped[str] = mapped_column(String(100))
    last_chat_datetime: Mapped[datetime] = mapped_column(DateTime)
    last_chat_summary: Mapped[str] = mapped_column(String(2000))
    last_chat_update_id: Mapped[int] = mapped_column(BigInteger)
