"""
    Handling message payload from user
"""
from math import ceil
from typing import Dict
import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException

from core.logger import LOG

from core.telegram.bot import TelegramBot
from core.ai import BOT_NAME, BOT_NICKNAME, BASE_PROMPT

from database.telegram import (
    get_telegram_user,
    insert_unauthorized_telegram_access,
    BotUserMessage
)

class MessagePayload(TelegramBot):
    def __init__(
        self, client: httpx.AsyncClient, payload: BotUserMessage,
        dbsession: Session
    ):
        super().__init__(client, payload)
        self.name = self.payload.chat.first_name
        self.dbsession = dbsession
        self.user_tele_id = self.payload.chat.id
        self.valid_user = get_telegram_user(self.user_tele_id, dbsession) or None

    async def ai_text_to_text_inquiry(
        self, async_ai_callback: callable, user_parts: Dict=None
    ) -> None:
        if self.valid_user is None:
            await self.unauthorized_access()

        if user_parts is None:
            user_parts = {
                'role': "user",
                'content': self.payload.text
            }
        resp = await async_ai_callback(
            user_parts,
            BASE_PROMPT.format(BOT_NAME, self.name, BOT_NICKNAME)
        )

        msg = resp.output.content.text

        chunks = ceil(len(msg)/4000)

        for idx in range(0,chunks):
            idx_next = (idx + 1) * 4000 # telegram max accept 4000 character
            msg = msg[(idx*4000):idx_next]
            if (idx+1) < chunks:
                msg += '--[Cont.]'
            await self.send_message_to_bot(message=msg)

        # TODO: insert to database

        return

    async def start_command_inquiry(self) -> None:
        """Start session with user. Since this command has a fix and static
        reply, we do not need to log the reply, we just log the user request"""
        LOG.info("User %s is starting the chat", self.name)
        msg = (
            f"Halo {self.name}. Aku {BOT_NAME} siap membantu. "
            f"Ada yang ingin ditanyakan? Kamu juga bisa tekan"
            f"/help untuk bantuan. \n\n-- ❤️‍🔥 {BOT_NAME}"
        )
        await self.send_message_to_bot(message= msg)
        LOG.info("Done introducing the bot...")

        if self.valid_user is None:
            insert_unauthorized_telegram_access(
                self.user_tele_id, self.payload.text, self.dbsession
            )

        return

    async def help_command_inquiry(self) -> None:
        """
            Help user using the bot. Since the command returns fix and static
            reply, we don't need to log the reply, just log the user request.
        """
        if self.valid_user is None:
            await self.unauthorized_access()

        LOG.info("User %s is requesting help.", self.name)
        msg = (
            f"Halo {self.name}. Kamu bisa bertanya apa saja yang kamu "
            f"ingin tanyakan kepadaku! Aku, {BOT_NAME} akan berusaha bantu."
            f"\n-- ❤️‍🔥 {BOT_NAME}"
        )
        await self.send_message_to_bot(message=msg)
        LOG.info("Done Sending the help!")

        # TODO: insert to database

        return

    async def unauthorized_access(self) -> HTTPException:
        LOG.info("Unauthorized user %s:%s is accessing data.", self.user_tele_id, self.name)
        msg = (
            f"Maaf {self.name}, saat ini {BOT_NICKNAME} hanya melayani Berlin dan "
            f"orang-orang tertentu saja. -- ❤️‍🔥 {BOT_NAME}"
        )
        await self.send_message_to_bot(message= msg)

        insert_unauthorized_telegram_access(
            self.user_tele_id, self.payload.text, self.dbsession
        )

        raise HTTPException(403)
