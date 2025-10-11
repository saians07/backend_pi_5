# pylint: disable=C0114
from fastapi import FastAPI, HTTPException, status
import httpx
from api import telegram_router
from core.logger import LOG
from core.telegram import TelegramBot

LOG.info("Starting Backend Pi 5 Applications ...")

async def lifespan(app: FastAPI):
    client = httpx.AsyncClient()
    bot = TelegramBot(client)
    app.state.bot = bot
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
