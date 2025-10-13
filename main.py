# pylint: disable=C0114
from fastapi import FastAPI, HTTPException, status
import httpx
from api import telegram_router
from core.logger import LOG
from database.base import DBSession
from core.telegram import TelegramBot

LOG.info("Starting Backend Pi 5 Applications ...")

# pylint: disable=W0621
async def lifespan(app: FastAPI):
    """Ensure the object will only be expanded once"""
    client = httpx.AsyncClient()
    bot = TelegramBot(client)
    app.state.bot = bot
    app.state.dbsession = DBSession()
    yield
    await client.aclose()

app = FastAPI(title="Backend Raspberry Pi", lifespan=lifespan)

@app.get("/", status_code=status.HTTP_403_FORBIDDEN)
def root():
    """Visit root path"""
    raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/health")
def health():
    """Check health for the page"""
    return {'status': "ok", 'status_code': status.HTTP_200_OK}

# include telegram route
app.include_router(telegram_router)
