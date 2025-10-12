# pylint: disable=C0114
from typing import Optional, List, Any
from pydantic import BaseModel, Field

class BotWebhook(BaseModel):
    """Parsing Raw Webhook URL From User"""
    url: str

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

class BotMessageBase(BaseModel):
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

class BotMessage(BotMessageBase):
    """When quote a reply, parsing the reply to message"""
    reply_to_message: Optional[BotMessageBase] = None

class BotMessageInput(BaseModel):
    """
        Parsing message directly accepted from user
        Source: https://core.telegram.org/bots/api#chatmemberupdated
    """
    update_id: int
    message: Optional[BotMessage] = None
    edited_message: Optional[Any] = None
    channel_post: Optional[Any] = None
    edited_channel_post: Optional[Any] = None
    business_connection: Optional[Any] = None
    business_message: Optional[BotMessage] = None
    edited_business_message: Optional[BotMessage] = None
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
