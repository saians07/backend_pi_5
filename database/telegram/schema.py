# pylint: disable=C0114, R0903, E1102
from datetime import datetime
from typing import (
    Optional,
    List,
    Any
)
from pydantic import BaseModel, Field
from sqlalchemy import (
    ForeignKey,
    String,
    BigInteger,
    Integer,
    Boolean,
    DateTime,
    Text,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from database.internal import Base

class BotChatHistory(Base):
    """Model to handle Chat History"""
    __tablename__ = 'telegram_bot_chat_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[str] = mapped_column(String(100))
    update_id: Mapped[int] = mapped_column(BigInteger)
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('telegram_bot_user.id'))
    role: Mapped[str] = mapped_column(String(20)) # user or model name
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    link_media: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
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

class BotBasePayload(BaseModel):
    """Parsing Raw Webhook URL From User"""
    url: Optional[str] = None
    user_id: Optional[int] = None

class BotChat(BaseModel):
    """Parsing key chat from message input"""
    id: int
    first_name: str
    username: Optional[str] = None
    type: str

class BotFromUserInfo(BaseModel):
    """Parsing key `from` from message input"""
    id: int
    is_bot: bool
    first_name: str
    username: Optional[str] = None
    language_code: Optional[str] = None

class BotPhoto(BaseModel):
    """Parsing key photo from message input"""
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int

class BotDocumentPhoto(BaseModel):
    """Parsing key document from message input"""
    file_name: str
    mime_type: str
    thumbnail: Optional[BotPhoto] = None
    thumb: Optional[BotPhoto] = None
    file_id: str
    file_unique_id: str
    file_size: int

class BotEntities(BaseModel):
    """Parsing key entities from message input"""
    offset: int
    length: int
    type_: str = Field(..., alias="type")

class BotUserMessageBase(BaseModel):
    """Parsing base message from message input"""
    message_id: int
    from_: BotFromUserInfo = Field(..., alias="from")
    chat: BotChat
    date: int
    text: Optional[str] = None
    photo: Optional[List[BotPhoto]] = None
    document: Optional[BotDocumentPhoto] = None
    caption: Optional[str] = None
    entities: Optional[List[BotEntities]] = None

class BotUserMessage(BotUserMessageBase):
    """When quote a reply, parsing the reply to message"""
    reply_to_message: Optional[BotUserMessageBase] = None

class BotMessageInput(BaseModel):
    """
        Parsing message directly accepted from user
        Source: https://core.telegram.org/bots/api#chatmemberupdated
    """
    update_id: int
    message: Optional[BotUserMessage] = None
    edited_message: Optional[Any] = None
    channel_post: Optional[Any] = None
    edited_channel_post: Optional[Any] = None
    business_connection: Optional[Any] = None
    business_message: Optional[BotUserMessage] = None
    edited_business_message: Optional[BotUserMessage] = None
    deleted_business_message: Optional[Any] = None
    message_reaction: Optional[Any] = None
    message_reaction_count: Optional[Any] = None
    inline_query: Optional[Any] = None
    chosen_inline_result: Optional[Any] = None
    callback_query: Optional[Any] = None
    shipping_query: Optional[Any] = None
    pre_checkout_query: Optional[Any] = None
    purchased_paid_media: Optional[Any] = None
    poll: Optional[Any] = None
    poll_answer: Optional[Any] = None
    my_chat_member: Optional[Any] = None
    chat_member : Optional[Any] = None
    chat_join_request: Optional[Any] = None
    chat_boost: Optional[Any] = None
    removed_chat_boost: Optional[Any] = None


class UnauthorizedUser(Base):
    """Model to record unauthorized users"""
    __tablename__ = 'telegram_unauthorized_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # user tele has no dedicated user id
    user_tele_id: Mapped[int] = mapped_column(BigInteger)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    link_media: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    created_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_datetime: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
