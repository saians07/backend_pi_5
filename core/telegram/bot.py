# pylint: disable=C0114
import os
from dotenv import load_dotenv
import httpx
from fastapi import HTTPException

load_dotenv()

BOT_TOKEN = os.getenv("TBOTAPI")
BACKEND_URL = os.getenv("BACKEND_URL")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
BASE_FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}"

if not BOT_TOKEN:
    raise RuntimeError("Missing TBOTAPI in env")

if not BACKEND_URL:
    raise RuntimeError("Missing BACKEND_URL in env")

bot_headers = {"Accept": "application/json"}

class TelegramBot:
    """Bot Client"""
    def __init__(self, client: httpx.AsyncClient):
        """Bot constructor"""
        self.client = client
        self._name = ""

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

    async def set_webhook(self, url: str) -> bool:
        """
        Assign a webhook into our bot. Afer assigning
        """
        try:
            r = await self.client.post(f"{BASE_URL}/setWebhook", params={'url': url}, timeout=5.0)
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


    async def send_message_to_bot(self, chat_id: str, message: str) -> dict | HTTPException:
        """Send back message to bot"""
        message = await self.client.post(
            f"{BASE_URL}/sendMessage",
            params={"chat_id": chat_id, "text": message, 'parse_mode': "MarkdownV2"},
            headers={"Content-Type":"application/json"}
        )
        if message.status_code != 200:
            raise HTTPException(message.status_code)

        return message.json()
