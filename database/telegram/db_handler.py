from sqlalchemy.orm import Session
from database.telegram.schema import (
    BotChatHistory,
    BotUserMapping,
    BotMessageInput,
    BotUserSummary,
    UnauthorizedUser
)

def get_telegram_user(
    user_tele_id: int, dbsession: Session
) -> BotUserMapping | None:
    user = dbsession.query(BotUserMapping).filter(
        BotUserMapping.user_tele_id == user_tele_id
    ).all()

    if len(user) != 1:
        return

    return user

def insert_unauthorized_telegram_access(
    user_tele_id : int, text: str, dbsession: Session
) -> None:
    unauthorize = UnauthorizedUser(
        user_tele_id=user_tele_id,
        text=text
    )
    dbsession.add(unauthorize)
    dbsession.commit()
    
    return

def insert_into_telegram_chat_history(
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

def summary_telegram_user_activity(payload: BotMessageInput, dbsession: Session) -> None:
    # TODO: Simpan data bot user summary
    pass
