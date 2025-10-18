# pylint: disable=C0114
import os
from typing import Union
from dotenv import load_dotenv
import httpx
from fastapi import HTTPException
from database.telegram import (
    BotUserMessage, BotMessageInput, BotBasePayload
)
from core.logger import LOG

from utils import telegram_message_escaper, telegram_message_smart_escaper

load_dotenv()

BOT_TOKEN = os.getenv("TBOTAPI")
BACKEND_URL = os.getenv("BACKEND_URL")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
BASE_FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}"

if not BOT_TOKEN:
    raise RuntimeError("Missing TBOTAPI in env")

if not BACKEND_URL:
    raise RuntimeError("Missing BACKEND_URL in env")

bot_headers = {
    "Accept": "application/json",
    "Content-Type":"application/json"
}

class TelegramBot:
    """Bot Client"""
    def __init__(
        self, client: httpx.AsyncClient,
        payload: Union[
            BotUserMessage, BotMessageInput, BotBasePayload
        ]
    ):
        """Bot constructor"""
        self.client = client
        self._name = ""
        self.payload = payload

    async def get_name(self) -> str:
        """Get the name of the bot"""
        try:
            request = await self.client.get(f"{BASE_URL}/getMe")
            request.raise_for_status()
            self._name = request.json().get("result").get("first_name")
            if not self._name:
                raise ValueError("There is no bot name found!")

            return self._name

        except HTTPException as e:
            raise e

    async def set_webhook(self) -> bool:
        """
        Assign a webhook into our bot. Afer assigning
        """
        try:
            r = await self.client.post(
                f"{BASE_URL}/setWebhook",
                params={'url': self.payload.url},
                timeout=5.0
            )
            r.raise_for_status()
            data = r.json()
            return data.get("ok", False)
        except Exception as e:
            raise e

    async def get_current_webhook(self) -> dict:
        """Check if the current bot already connected to a webhook"""
        try:
            result = await self.client.get(f"{BASE_URL}/getWebhookInfo")
            result.raise_for_status()
            return result.json()
        except Exception as e:
            raise e

    async def delete_webhook(self) -> dict:
        """Remove current webhook from the bot!"""
        try:
            result = await self.client.get(f"{BASE_URL}/deleteWebhook")
            result.raise_for_status()
            return result.json()
        except Exception as e:
            raise e

    async def get_file_location(self, file_id: str) -> dict:
        """Grab file location from telegrams file server"""
        request = await self.client.get(f"{BASE_URL}/getFile", params={'file_id':file_id})
        request.raise_for_status()
        return request.json()

    async def get_file_data(self, file_id: str) -> bytes:
        """Grab the image data from telegram server"""
        location = await self.get_file_location(file_id)
        if location.json().get("error_code"):
            raise HTTPException(location.json().get("error_code"))

        img_path = location.get("result").get("file_path")
        img_response = await self.client.get(f"{BASE_FILE_URL}/{img_path}")

        if img_response.status_code != 200:
            raise HTTPException(img_response.status_code)

        img_data = img_response.content
        return img_data

    async def get_chat_id(self):
        """
            Payload can be either:
                BotUserMessage,
                BotMessageInput,
                BotBasePayload
            For each object, the chat id might be availabe or not available.
            Hence, we have to be careful and check the type when extracting it.
        """
        chat_id = None
        if isinstance(self.payload, BotUserMessage):
            chat_id = self.payload.chat.id
        elif isinstance(self.payload, BotMessageInput):
            chat_id = self.payload.message.chat.id
        elif isinstance(self.payload, BotBasePayload):
            raise ValueError("Payload of BotUserMessage, has not chat_id")
        
        return chat_id


    async def send_message_to_bot(self, message: str) -> dict | HTTPException:
        """Send back message to bot"""
        LOG.info("Sending message to user: %s...", message[0:100])
        text = await telegram_message_smart_escaper(message)
        LOG.info("%s", text)
        text = await self.client.post(
            f"{BASE_URL}/sendMessage",
            params={
                "chat_id": await self.get_chat_id(),
                "text": text,
                'parse_mode': "MarkdownV2"
            },
            headers=bot_headers
        )
        LOG.info("%s", text.content)
        if text.status_code != 200:
            text = await telegram_message_escaper(message)
            text = await self.client.post(
                f"{BASE_URL}/sendMessage",
                params={
                    "chat_id": await self.get_chat_id(),
                    "text": text,
                    'parse_mode': "MarkdownV2"
                },
                headers=bot_headers
            )
            
        if text.status_code != 200:
            raise HTTPException(message.status_code, "Error sending message to users.")

        LOG.info("Done sending message to user.")

        return text.json()
