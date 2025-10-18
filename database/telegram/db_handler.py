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

    return user[0]

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
    update_id: int, user_tele_id: int,
    text: str, role: str, session_id: str,
    dbsession: Session, link_media: str=None
) -> None:
    user_ = get_telegram_user(user_tele_id, dbsession)

    chat_history = BotChatHistory(
        update_id=update_id,
        user_id=user_.id,
        session_id=session_id,
        role=role,
        text=text,
        link_media=link_media
    )
    dbsession.add(chat_history)
    dbsession.commit()

    return

def insert_telegram_user_summary(payload: BotMessageInput, dbsession: Session) -> None:
    # TODO: Simpan data bot user summary
    pass
