# pylint: disable=C0114, W0511, R0912
from fastapi import APIRouter
from sqlalchemy.orm import Session
from core.logger import LOG
from core.telegram import (
    BotMessageInput,
    TelegramBot,
    MessagePayload
)

router = APIRouter(prefix="/telegram", tags=["telegram"])

async def bot_assistant(payload: BotMessageInput, bot: TelegramBot, dbsession: Session) -> None:
    """
        Process all input from users.
        Return only string data, None when there is no
    """
    if payload.message:
        LOG.info("Forwarding message to message handler ...")
        user_message = MessagePayload(bot.client, payload.message)
        if user_message.payload.message.chat:
            await user_message.user_message_handler(dbsession)
        return

    if payload.edited_message:
        LOG.info("A user is editing their message ...")
        return

    return
