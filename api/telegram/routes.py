# pylint: disable=C0114
from typing import AsyncGenerator, Union
from fastapi import APIRouter, status, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from core.telegram import (
    BotMessageInput,
    TelegramBot,
    BotBasePayload,
    BASE_API
)
from core.logger import LOG
from database.base import DBSession
from api.telegram.bot_handler import bot_assistant

async def get_bot(
    request: Request,
    payload: Union[BotBasePayload, BotMessageInput]=None
) -> TelegramBot:
    """Get state of the bot from main app"""
    httpx_client = request.app.state.httpx_client
    bot = TelegramBot(client=httpx_client, payload=payload)
    return bot

async def get_db_session() -> AsyncGenerator[Session, None]:
    dbsession = DBSession()
    try:
        yield dbsession
    finally:
        dbsession.close()

telegram_router = APIRouter(prefix=f"{BASE_API}/telegram")

@telegram_router.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook(payload: BotMessageInput, bot: TelegramBot=Depends(get_bot), dbsession: Session=Depends(get_db_session)):
    """Endpoint where telegram will receive direct input for the bot!"""
    LOG.info("receiving new payload \n %s", payload)

    await bot_assistant(payload, bot, dbsession)

    return {
        'status': status.HTTP_202_ACCEPTED,
        'message': "Your request has been accepted."
    }

@telegram_router.post("/set_webhook", status_code=status.HTTP_200_OK)
async def set_telegram_webhook(payload: BotBasePayload=None, bot: TelegramBot=Depends(get_bot)):
    """Set the telegram webhook to new webhook"""
    # check if there is url in the payload
    if not payload or not payload.url:
        raise HTTPException(400)

    url = payload.url

    # always use try catch block
    try:
        curr_webhook = await bot.get_current_webhook()
        # first, we need to check if there is an active webhook
        if curr_webhook.get("result").get("url"):
            raise HTTPException(
                400,
                "There is an active webhook attached to the bot. \
                    Delete it first!"
            )

        # only set the webhook when there is no active webhook attached
        is_webhooked = await bot.set_webhook()
        if not is_webhooked:
            raise HTTPException(400, "Bad Request!")

        return {
            'status': "Success",
            'message': f"You have successfully attach {url} to the bot!",
            'status_code': status.HTTP_200_OK
        }

    except Exception as e:
        raise e

@telegram_router.get("/get_webhook", status_code=status.HTTP_200_OK)
async def get_telegram_webhook(bot: TelegramBot=Depends(get_bot)):
    """Get telegram webhook connected to the bot"""
    try:
        curr_webhook = await bot.get_current_webhook()
        if not curr_webhook.get("result").get("url"):
            raise HTTPException(404)

        return curr_webhook

    except Exception as e:
        raise e

@telegram_router.get("/delete_webhook", status_code=status.HTTP_200_OK)
async def delete_telegram_webhook(bot: TelegramBot=Depends(get_bot)):
    """Delete the webhook connected to the bot"""
    try:
        res = await bot.delete_webhook()
        return {'message': res.get("description"), 'status_code': status.HTTP_200_OK}
    except Exception as e:
        raise e
