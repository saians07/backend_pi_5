"""
    Handling message payload from user
"""
from math import ceil
import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException

from core.logger import LOG

from core.telegram.bot import TelegramBot
from core.telegram.schema import BotUserMessage
from core.ai import BOT_NAME, BOT_NICKNAME, BASE_PROMPT

from database.telegram import get_telegram_user

from api.ai import ask_gemini

class MessagePayload(TelegramBot):
    def __init__(self, client: httpx.AsyncClient, payload: BotUserMessage):
        super().__init__(client, payload)

    async def user_message_handler(self, dbsession: Session) -> None:
        user_id = self.payload.from_.id

        # We simply use first name since not everyone set their username
        # or complete name
        name = self.payload.from_.first_name

        valid_user = get_telegram_user(user_id, dbsession) or None

        # do not put any return on this check.
        # it must go through when the type is not bot command.
        if self.payload.entities:
            entities = self.payload.entities
            bot_command = [
                ent.type_ == "bot_command" for ent in entities
            ]
            if any(bot_command):
                # except /start, reply everything using user_command_handler
                if self.payload.text == "/start":
                    msg = (
                        f"Halo {name}. Aku {BOT_NAME} siap membantu. "
                        f"Ada yang ingin ditanyakan? -- ❤️‍🔥 {BOT_NAME}"
                    )
                    await self.send_message_to_bot(
                        message= msg
                    )
                    LOG.info("Done starting the chat!")
                    return

                if valid_user is not None:
                    await self.user_command_handler(self.payload.text, name)
                    return
                else:
                    await self.unauthorized_access(name, user_id)
        
        # now, we get a condition where this is just a casual message from users.
        # Not a bot command
        if valid_user is None:
            await self.unauthorized_access(name, user_id)

        if self.payload.text:
            msg = await self.text_message_handler(self.payload.text, name)

            chunks = ceil(len(msg)/4000)
            LOG.info("Message from gemini: %s...", msg[0:100])
            for idx in range(0,chunks):
                idx_next = (idx + 1) * 4000 # telegram max accept 4000 character
                msg = msg[(idx*4000):idx_next]
                if (idx+1) < chunks:
                    msg += '--[Cont.]'
                await self.send_message_to_bot(message=msg)

            return

    async def text_message_handler(self, text: str, name: str):
        user_parts = {
            'role': "user",
            'content': text
        }
        resp = await ask_gemini(
            user_parts,
            BASE_PROMPT.format(BOT_NAME, name, BOT_NICKNAME)
        )

        return resp.output.content.text

    async def user_command_handler(
        self, command: str, name: str
    ) -> None:
        """Handling user command other than start"""
        if command == "/help":
            msg = (
                f"Halo {name}. Kamu bisa bertanya apa saja yang kamu "
                f"ingin tanyakan kepadaku! Aku, {BOT_NAME} akan berusaha bantu."
            )

            await self.send_message_to_bot(
                message=msg
            )
            LOG.info("Done Sending the help!")
        
        return

    async def unauthorized_access(self, name: str, user_id: int) -> HTTPException:
        LOG.info("Unauthorized user %s:%s is accessing data.", user_id, name)
        msg = (
            f"Maaf {name}, saat ini {BOT_NICKNAME} hanya melayani Berlin dan "
            f"orang-orang tertentu saja. -- ❤️‍🔥 {BOT_NAME}"
        )
        await self.send_message_to_bot(message= msg)

        raise HTTPException(403)
