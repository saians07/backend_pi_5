from pydantic import BaseModel, Field
from typing import Optional, List

class BotWebhook(BaseModel):
    """Parsing Raw Webhook URL From User"""
    url: str

class BotChat(BaseModel):
    """Parsing key chat from message input"""
    id: int
    first_name: str
    username: str
    type: str

class BotFromUserInfo(BaseModel):
    """Parsing key `from` from message input"""
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str

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
    """Parsing message directly accepted from user"""
    update_id: int
    message: Optional[BotMessage] = None
