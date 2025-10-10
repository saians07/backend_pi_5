import os
from dotenv import load_dotenv
import httpx
from fastapi import HTTPException
from pydantic import BaseModel

load_dotenv()

BOT_TOKEN = os.getenv("TBOTAPI")
BACKEND_URL = os.getenv("BACKEND_URL")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

if not BOT_TOKEN:
    raise RuntimeError("Missing TBOTAPI in env")

if not BACKEND_URL:
    raise RuntimeError("Missing BACKEND_URL in env")

bot_headers = {"Accept": "application/json"}

class TelegramBot(BaseModel):

    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self._name = ""

    async def get_name(self, header: dict=bot_headers) -> str:
        try:
            request = await self.client.get(f"{BASE_URL}/getMe")
            request.raise_for_status()
            self._name = request.json().get("result").get("first_name")
            if self._name:
                return
            else:
                raise ValueError("There is no bot name found!")
        except Exception as e:
            raise e

    async def set_webhook(self, url: str) -> bool:
        """
        Assign a webhook into our bot. Afer assigning
        """
        try:
            r = await self.client.post(f"{BASE_URL}/setWebhook", json={'url': url}, timeout=5.0)
            r.raise_for_status()
            data = r.json()
            return data.get("ok", False)
        except Exception as e:
            raise e

    async def get_current_webhook(self):
        try:
            result = await self.client.get(f"{BASE_URL}/getWebhookInfo")
            result.raise_for_status()
            return result.json()
        except Exception as e:
            raise e

    async def delete_webhook(self):
        try:
            result = await self.client.get(f"{BASE_URL}/deleteWebhook")
            result.raise_for_status()
            return result.json()
        except Exception as e:
            raise HTTPException(500, str(e))