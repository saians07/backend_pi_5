# pylint: disable=C0114, W0511, R0912
from fastapi import APIRouter
from sqlalchemy.orm import Session
from api.ai import ask_gemini
from core.logger import LOG
from core.telegram import TelegramBot, MessagePayload
from database.telegram import (
    BotMessageInput
)

router = APIRouter(prefix="/telegram", tags=["telegram"])

async def bot_assistant(payload: BotMessageInput, bot: TelegramBot, dbsession: Session) -> None:
    """
        Process all input from users.
        Return only string data, None when there is no
    """

    if payload.message:
        LOG.info("Handling messages")

        # if the payload has messages from user, then first create the object
        # this object will help us to work with
        user_message = MessagePayload(
            bot.client, payload.message, payload.update_id, dbsession=dbsession
        )

        # handling entity
        # entities can be a command, can be a position of formatting
        # we need to fetch if the `entities` is a specific command to do!
        # DO NOT put any return on `entities` check but for each command!
        if user_message.payload.entities:
            entities = user_message.payload.entities
            bot_command = [
                entity.type_ == 'bot_command' for entity in entities
            ]
            if any(bot_command):
                if user_message.payload.text == "/start":
                    await user_message.start_command_inquiry()
                    return
                elif user_message.payload.text == "/help":
                    await user_message.help_command_inquiry()
                    return

        if user_message.payload.text:
            await user_message.ai_text_to_text_inquiry(async_ai_callback=ask_gemini)
            return
        
        if user_message.payload.photo:
            return

        return

    if payload.edited_message:
        LOG.info("A user is editing their message ...")
        return

    return
