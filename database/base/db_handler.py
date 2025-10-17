from sqlalchemy.orm import Session
from database.telegram.schema import (
    BotChatHistory,
    BotUserMapping,
    BotUserSummary
)
from core.telegram.schema import BotMessageInput

def validate_user(user_id: int, dbsession: Session) -> str | None:
    bot_user = dbsession.query(BotUserMapping).filter(BotUserMapping.id == user_id).all()

    # ensure there is only 1 user id found
    if len(bot_user) != 1:
        return False

    return True

def get_telegram_user(
    user_id: int,
    dbsession: Session
) -> BotUserMapping:
    user = dbsession.query(BotUserMapping).filter(
        BotUserMapping.user_tele_id == user_id
    ).all()

    if len(user) != 1:
        return

    return user

def insert_into_tele_chat_history(
    payload: BotMessageInput, dbsession: Session, role: str
) -> None:
    user_id = payload.message.from_.id
    if get_telegram_user(payload.message.from_.id) is None:
        return
    chat_history = BotChatHistory(
        update_id = payload.update_id,
        user_id = user_id,
        role = role
    )
    dbsession.add(chat_history)
    dbsession.commit()

    return

def BotUserSummary(payload: BotMessageInput, dbsession: Session) -> None:
    # TODO: Simpan data bot user summary
    pass
