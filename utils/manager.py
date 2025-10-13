"""
    Inject all clients, object classes, and tables needed by the main application
"""
from fastapi import FastAPI
import httpx
from core.telegram import TelegramBot
from database.base import DBSession, Base, engine
from database.telegram_bot_chat import (
    BotChatHistory,
    BotUserMapping,
    BotUserSummary
)

async def lifespan(app: FastAPI):
    """
        Preparing objects and clients for each fastapi worker
    """
    httpx_client = httpx.AsyncClient()
    bot = TelegramBot(client=httpx_client)
    app.state.bot = bot

    dbsession = DBSession()
    app.state.dbsession = dbsession
    yield
    await httpx_client.aclose()
    await dbsession.close()

def create_all_table():
    Base.metadata.create_all(engine)
