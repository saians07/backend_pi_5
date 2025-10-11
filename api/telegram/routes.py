# pylint disable: C0114
from fastapi import APIRouter 
from api.telegram.bot_handler import router

BASE_API = "/api/v1"

telegram_router = APIRouter(prefix=f"{BASE_API}")

telegram_router.include_router(router)
