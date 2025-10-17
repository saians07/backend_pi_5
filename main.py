# pylint: disable=C0114
from fastapi import FastAPI
from api import (
    telegram_router,
    internal_router
)
from core.logger import LOG
from utils.manager import lifespan

LOG.info("Starting Backend Pi 5 Applications ...")

app = FastAPI(title="Backend Raspberry Pi", lifespan=lifespan)

# include all routes
app.include_router(internal_router)
app.include_router(telegram_router)
