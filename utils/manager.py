# pylint: disable=W0611
"""
    Inject all clients, object classes, and tables needed by the main application
"""
from fastapi import FastAPI
import httpx
from core.telegram import TelegramBot

async def lifespan(app: FastAPI):
    """
        Preparing objects and clients for each fastapi worker
    """
    httpx_client = httpx.AsyncClient()
    bot = TelegramBot(client=httpx_client)
    app.state.bot = bot

    yield
    await httpx_client.aclose()
