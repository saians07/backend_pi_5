"""Init for database/base"""
from database.base.client import (
    DBSession,
    engine,
    DATABASE_URL
)
from database.base.schema import Base
from database.base.handler import get_telegram_user
